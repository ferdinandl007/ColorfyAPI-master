import logging

import azure.functions as func

import os
os.environ['TORCH_HOME'] = '.'

from .deoldify.visualize import *

import base64

plt.style.use('dark_background')
torch.backends.cudnn.benchmark=True

colorizer = get_azure_artistic_image_colorizer()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')    

    logging.error(dir(blobout.get()))

    source_url = None
    render_factor = 30  #@param {type: "slider", min: 7, max: 45}
    watermarked = True #@param {type:"boolean"}

    encoded_source_url = req.params.get("encoded_source_url")
    if encoded_source_url:
        source_url = base64.b64decode(encoded_source_url)       

    render_factor_param = req.params.get("render_factor")
    if render_factor_param:
        try:
            render_factor = int(render_factor_param)
        except:
            render_factor = render_factor

    logging.info("Start colorising with source url: {0}, render_factor: {1}".format(source_url, render_factor)) 

    if source_url is not None and source_url !='':
        colorised_img = colorizer.get_transformed_image_from_url(
            url=source_url, 
            render_factor=render_factor, 
            watermarked=watermarked
        )
    else:
        return func.HttpResponse(
            "Please pass in a valid source_url",
            status_code=400
        )

    output_img_byte_arr = io.BytesIO()
    # Convert composite to RGB so we can save as JPEG
    colorised_img.convert('RGB').save(output_img_byte_arr, format='JPEG')

    save_img = req.params.get("save_img")
    # if save_img:        
    #     blobout.set(output_img_byte_arr.getvalue())    


    return_img = req.params.get('return_img')
    if return_img:

        headers={
            "Content-Type":"image/jpeg"
        }

        return func.HttpResponse(
            output_img_byte_arr.getvalue(),
            headers = headers
        )
    else:
        return func.HttpResponse(
            "No image needs to be returned"
        )

