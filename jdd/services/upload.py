# -*- coding=utf-8
# 腾讯云COSV5Python SDK
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError
import sys
import logging
def upload_cos(user_id,file_name,file_path,**kwargs):
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    secret_id = 'AKIDd8Sin6KBSckkkZse1IOJ2b4Sfo49O4va'     
    secret_key = 'eDcqunYBd0CKNF1mRNBrT2Uo152rncJt'     
    region = 'ap-hongkong'    
    token = None             
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  
    client = CosS3Client(config)
    response = client.upload_file(Bucket='jdiandian-1257713877', LocalFilePath= file_path, Key=str(user_id) +'/'+ file_name, PartSize=10, MAXThread=10)
    # flash(response['ETag'])

    


