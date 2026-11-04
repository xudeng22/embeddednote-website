import test from 'node:test';
import assert from 'node:assert/strict';
import {PRESETS, parsePalette,convertRGBA,packed4,unpacked8,validateOptions,MAX_PIXELS} from '../src/lib/epaper-image.mjs';
const o=(more={})=>({width:1,height:1,method:'nearest',palette:PRESETS.four.colors,...more});
const rgba=(...pixels)=>Uint8ClampedArray.from(pixels.flatMap(p=>[...p,255]));
test('palettes have 4, 6, 8 distinct entries',()=>{for(const [k,n] of [['four',4],['six',6],['eight',8]]){const a=parsePalette(PRESETS[k].colors);assert.equal(a.length,n);assert.equal(new Set(a.map(x=>x.hex)).size,n);}});
test('black and white map exactly for all palettes',()=>{for(const p of Object.values(PRESETS)){const r=convertRGBA(rgba([0,0,0],[255,255,255]),o({width:2,palette:p.colors}));assert.deepEqual(Array.from(r.indices),[0,1]);}});
test('four palette exact red and yellow',()=>{const r=convertRGBA(rgba([255,0,0],[255,255,0]),o({width:2}));assert.deepEqual(Array.from(r.indices),[2,3]);});
test('six palette exact blue and green',()=>{const r=convertRGBA(rgba([0,0,255],[0,255,0]),o({width:2,palette:PRESETS.six.colors}));assert.deepEqual(Array.from(r.indices),[4,5]);});
test('eight palette exact cyan and magenta',()=>{const r=convertRGBA(rgba([0,255,255],[255,0,255]),o({width:2,palette:PRESETS.eight.colors}));assert.deepEqual(Array.from(r.indices),[6,7]);});
test('transparent pixel becomes white',()=>{const r=convertRGBA(Uint8ClampedArray.from([0,0,0,0]),o());assert.equal(r.indices[0],1);});
test('packed4 uses even high nibble and odd low nibble',()=>assert.deepEqual(Array.from(packed4(Uint8Array.from([1,2,3]))),[0x12,0x30]));
test('unpacked8 preserves codes',()=>assert.deepEqual(Array.from(unpacked8([0,7,2])),[0,7,2]));
test('modes generate only allowed indices and preserve dimensions',()=>{for(const mode of ['nearest','floyd','atkinson','bayer']){const r=convertRGBA(rgba([123,89,42],[187,44,99],[22,22,22],[220,220,220]),o({width:2,height:2,method:mode,palette:PRESETS.six.colors}));assert.equal(r.rgba.length,16);assert.equal(r.histogram.reduce((a,b)=>a+b,0),4);assert.ok(Array.from(r.indices).every(x=>x<6));}});
test('same inputs are deterministic',()=>{const input=rgba(...Array.from({length:25},(_,i)=>[i*10,i*7,i*4]));for(const mode of ['floyd','atkinson','bayer']){const a=convertRGBA(input,o({width:5,height:5,method:mode}));const b=convertRGBA(input,o({width:5,height:5,method:mode}));assert.deepEqual(a.indices,b.indices);}});
test('invalid palette hex fails',()=>assert.throws(()=>parsePalette([{hex:'#000000'},{hex:'#GGGGGG'}])));
test('invalid output bounds fail',()=>assert.throws(()=>validateOptions(o({width:3000,height:3000}))));
test('zero and non-integer sizes fail',()=>{for(const width of [0,-1,2.5])assert.throws(()=>validateOptions(o({width})));});
test('wrong pixel buffer length fails',()=>assert.throws(()=>convertRGBA(new Uint8ClampedArray(5),o())));
test('invalid method and adjustment fail',()=>{assert.throws(()=>validateOptions(o({method:'unknown'})));assert.throws(()=>validateOptions(o({saturation:-1})));});
test('4-bit pack refuses out-of-range index',()=>assert.throws(()=>packed4(Uint8Array.from([16]))));
test('boundary maximum pixels accepted',()=>{assert.equal(validateOptions(o({width:3000,height:2000})).length,4);assert.equal(MAX_PIXELS,6000000);});
test('histogram exact for 2x2 known pixels',()=>{const r=convertRGBA(rgba([0,0,0],[0,0,0],[255,255,255],[255,0,0]),o({width:2,height:2}));assert.deepEqual(r.histogram,[2,1,1,0]);});

// v1.1 regression tests: CIE Lab, measured device profiles and neutral edge preservation.
import {DISPLAY_PROFILES,createProfile,validateProfile,profilePalette,rgbToLab,deltaE76} from '../src/lib/epaper-image.mjs';
test('D65 sRGB Lab anchors are accurate within tolerance',()=>{
 const white=rgbToLab(255,255,255), black=rgbToLab(0,0,0),red=rgbToLab(255,0,0);
 assert.ok(Math.abs(white[0]-100)<0.002);assert.ok(Math.abs(black[0])<0.002);
 assert.ok(Math.abs(red[0]-53.2408)<0.1);assert.ok(Math.abs(red[1]-80.0925)<0.2);
 assert.ok(deltaE76(white,white)<1e-10);
});
test('reference profiles validate with explicit native index mapping',()=>{
 for(const profile of Object.values(DISPLAY_PROFILES)) {
 const p=validateProfile(profile);
 assert.equal(p.measured,false);assert.equal(profilePalette(p).length,p.colors.length);
 assert.deepEqual(p.colors.map(c=>c.code),p.colors.map((_,i)=>i));
 }
});
test('measured profile display color does not overwrite native ink color',()=>{
 const p=createProfile('demo','Demo', [{name:'Black',hex:'#000000',measuredHex:'#202020'},{name:'White',hex:'#FFFFFF',measuredHex:'#EAE3D6'},{name:'Red',hex:'#FF0000',measuredHex:'#BB4035'},{name:'Yellow',hex:'#FFFF00',measuredHex:'#C4AA39'}],true);
 const pal=profilePalette(p);
 assert.equal(pal[1].hex,'#EAE3D6');assert.equal(pal[1].nativeHex,'#FFFFFF');assert.equal(pal[1].nativeCode,1);
});
test('reject duplicate native codes and unsupported schema',()=>{
 const profile=structuredClone(DISPLAY_PROFILES.four);
 profile.colors[1].code=profile.colors[0].code;
 assert.throws(()=>validateProfile(profile),/unique/);
 profile.colors[1].code=1;profile.schemaVersion=7;
 assert.throws(()=>validateProfile(profile),/schemaVersion/);
});
test('Lab matching determinism for all dithering modes',()=>{
 const input=rgba(...Array.from({length:64},(_,i)=>[i*3,i*2,255-i*3]));
 for(const method of ['nearest','floyd','atkinson','bayer']){
  const opts=o({width:8,height:8,method,palette:PRESETS.six.colors,matching:'lab'});
  assert.deepEqual(convertRGBA(input,opts).indices,convertRGBA(input,opts).indices);
 }
});
test('neutral text edges become clean binary pixels with edge mode',()=>{
 const data=rgba(...Array.from({length:25},(_,i)=>((i%5===2)?[20,20,20]:[240,240,240])));
 const opts=o({width:5,height:5,palette:PRESETS.four.colors,method:'floyd',matching:'lab',edgeProtection:true,edgeThreshold:40});
 const result=convertRGBA(data,opts);
 for(let y=0;y<5;y++)assert.equal(result.indices[y*5+2],0);
});
test('edge mode does not force saturated red strokes to black/white',()=>{
 const data=rgba([255,0,0],[255,255,255],[255,0,0]);
 const r=convertRGBA(data,o({width:3,method:'nearest',edgeProtection:true,edgeThreshold:20}));
 assert.equal(r.indices[0],2);assert.equal(r.indices[2],2);
});
test('invalid matching and edge settings are rejected',()=>{
 assert.throws(()=>validateOptions(o({matching:'lab2000'})));
 assert.throws(()=>validateOptions(o({edgeProtection:'yes'})));
 assert.throws(()=>validateOptions(o({edgeThreshold:5})));
});

// v1.2: quality and format regressions.
import {computeToneFit} from '../src/lib/epaper-image.mjs';
test('photo tone fit has valid bounds and preserves opaque output',()=>{
 const input=rgba(...Array.from({length:64},(_,i)=>[40+i*2,50+i*2,60+i*2]));
 const fit=computeToneFit(input,8,8,parsePalette(PRESETS.six.colors));
 assert.ok(fit.lo<=fit.hi && fit.outLo<=fit.outHi);
 const baseline=convertRGBA(input,o({width:8,height:8,matching:'lab',method:'floyd',palette:PRESETS.six.colors}));
 const result=convertRGBA(input,o({width:8,height:8,matching:'lab',method:'floyd',palette:PRESETS.six.colors,toneFit:'photo'}));
 assert.equal(result.rgba.length,baseline.rgba.length);
 assert.equal(result.histogram.reduce((a,b)=>a+b,0),64);
 for(let i=3;i<result.rgba.length;i+=4) assert.equal(result.rgba[i],255);
});
test('unsupported tone mode rejected',()=> assert.throws(()=>validateOptions(o({toneFit:'fake'})),/tone fit/i));
test('atkinson serpentine remains deterministic with text protection',()=>{
 const input=rgba(...Array.from({length:91},(_,i)=>[i*19%256,i*13%256,i*7%256]));
 const opts=o({width:13,height:7,method:'atkinson',palette:PRESETS.eight.colors,edgeProtection:true});
 assert.deepEqual(convertRGBA(input,opts).indices,convertRGBA(input,opts).indices);
});
test('measured profile is used for display appearance while index stays native position',()=>{
 const p=createProfile('measured','Measured', [
  {name:'Black',hex:'#000000',measuredHex:'#171717'},
  {name:'White',hex:'#FFFFFF',measuredHex:'#F1EBDC'},
  {name:'Red',hex:'#FF0000',measuredHex:'#BB4040'},
  {name:'Yellow',hex:'#FFFF00',measuredHex:'#D9B55A'},
 ],true);
 const pal=profilePalette(p);
 const result=convertRGBA(rgba([187,64,64]),o({palette:pal,matching:'lab'}));
 assert.equal(result.indices[0],2);
 assert.deepEqual(Array.from(result.rgba.slice(0,3)),[187,64,64]);
});
