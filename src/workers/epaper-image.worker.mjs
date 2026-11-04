import {convertRGBA} from '../lib/epaper-image.mjs';
self.onmessage = event => {
  const {id,rgba,options}=event.data;
  try {
    const result=convertRGBA(new Uint8ClampedArray(rgba),options);
    self.postMessage({id,ok:true,indices:result.indices.buffer,rgba:result.rgba.buffer,histogram:result.histogram},[result.indices.buffer,result.rgba.buffer]);
  } catch(error) {
    self.postMessage({id,ok:false,error:String(error?.message || error)});
  }
};
