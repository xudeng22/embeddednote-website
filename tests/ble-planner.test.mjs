import test from 'node:test';
import assert from 'node:assert/strict';
import {calculateBlePlan, DEFAULTS} from '../src/lib/ble-planner.mjs';
test('baseline 240000 bytes, MTU 247, four writes/event',()=>{
 const r=calculateBlePlan();assert.equal(r.ok,true);assert.equal(r.netBytes,244);assert.equal(r.writes,984);assert.equal(r.events,246);assert.equal(r.transferMs,7380);assert.equal(r.perEvent,4);
});
test('ATT MTU 23 yields 20 B value',()=>{
 const r=calculateBlePlan({mtu:23,chunkBytes:244,phy:'1M',llPayload:27,eventMs:15});assert.equal(r.netBytes,20);assert.equal(r.writes,12000);assert.equal(r.fragmentsPerFullWrite,1);
});
test('application header subtracts from image bytes per write',()=>{
 const r=calculateBlePlan({appHeader:4});assert.equal(r.netBytes,240);assert.equal(r.writes,1000);assert.equal(r.appHeaderBytes,4000);
});
test('DLE off causes fragmentation',()=>{
 const r=calculateBlePlan({llPayload:27,eventMs:30,intervalMs:30});assert.equal(r.ok,true);assert.ok(r.fragmentsPerFullWrite>1);
});
test('request method slower than write command under default RTT',()=>{
 const a=calculateBlePlan();const b=calculateBlePlan({method:'request'});assert.ok(b.totalMs>a.totalMs);
});
test('larger setup plus processing included exactly',()=>{
 const r=calculateBlePlan({setupMs:500,processingMs:25});assert.equal(r.totalMs,r.transferMs+525);
});
test('invalid event duration cannot exceed connection interval',()=>{
 assert.equal(calculateBlePlan({eventMs:31,intervalMs:30}).ok,false);
});
test('reject empty net payload',()=>{
 assert.equal(calculateBlePlan({appHeader:20,chunkBytes:20}).ok,false);
});
test('reject invalid negative and nonnumeric input',()=>{
 assert.equal(calculateBlePlan({dataBytes:-10}).ok,false);
 assert.equal(calculateBlePlan({mtu:'not-a-number'}).ok,false);
});
test('last partial fragment is included',()=>{
 const r=calculateBlePlan({dataBytes:245});assert.equal(r.writes,2);assert.equal(r.lastNetBytes,1);assert.ok(r.airtimeMs>0);
});
test('encrypted payload fragments 251 byte total LL and not MTU size',()=>{
 const r=calculateBlePlan({mtu:517,chunkBytes:514,llPayload:251,eventMs:15});assert.equal(r.ok,true);assert.equal(r.fragmentsPerFullWrite,3);
});
test('retry penalty increases time',()=>{
 assert.ok(calculateBlePlan({retryPercent:15}).totalMs>calculateBlePlan().totalMs);
});
test('encrypted MTU247 fits one 251-byte LL data payload plus separate MIC',()=>{
 const r=calculateBlePlan(); assert.equal(r.fragmentsPerFullWrite,1);assert.ok(r.airtimeMs>0);
});
test('no encryption allows unfragmented MTU 23 with LL 27',()=>{
 const r=calculateBlePlan({mtu:23,llPayload:27,encryption:false});assert.equal(r.fragmentsPerFullWrite,1);
});
test('large header can reduce useful net payload and raise operations',()=>{
 const x=calculateBlePlan({appHeader:8});const y=calculateBlePlan();assert.ok(x.writes>y.writes);
});

test('four presets produce expected ATT operation counts',()=>{
 for (const [size,count] of [[240000,984],[1024,5],[262144,1075],[32768,135]]) {
  const r=calculateBlePlan({dataBytes:size}); assert.equal(r.ok,true); assert.equal(r.writes,count);
 }
});
test('MIC changes airtime but does not reduce LL data payload',()=>{
 const encrypted=calculateBlePlan({dataBytes:24400,encryption:true});
 const plain=calculateBlePlan({dataBytes:24400,encryption:false});
 assert.equal(encrypted.fragmentsPerFullWrite,1);
 assert.equal(plain.fragmentsPerFullWrite,1);
 assert.ok(encrypted.airtimeMs>plain.airtimeMs);
});
test('reject non-BLE connection interval and unsupported platform',()=>{
 assert.equal(calculateBlePlan({intervalMs:30.1}).ok,false);
 assert.equal(calculateBlePlan({platform:'unknown'}).ok,false);
});
