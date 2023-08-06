'''
该文档是一个总结性的，通过调用数据提供接口，可以下载该接口提供的图片数据，然后将这些数据调用要比较的算法
最后会得到一个汇总结果
'''
from yuncheng_util_pkg.util import get_for_request
from yuncheng_util_pkg.util_file import  down_pic
from yuncheng_util_pkg.compare_two_al_result import Get_result_and_compare
from yuncheng_util_pkg.compare_two_al_result import DecodeTheSummaryFile
def get_pics(url,savePath):
    result = get_for_request(url)
    pics = []
    for i in result['data']:
        picUrl = i['url']
        pic = down_pic(picUrl,savePath)
        pics.append(pic)
    return pics

def compare(pics,url1,url2,saveFile,url1ResultSavePath,url2ResultSavePath,decodeSavePath,useCache=True):
    com = Get_result_and_compare(url1,url2,pics,saveFile,useCache,url1ResultSavePath,url2ResultSavePath)
    com.compare_two_pic_local()
    com.summary()
    dif = DecodeTheSummaryFile(saveFile,decodeSavePath)
    dif.show_brand_dif()
    dif.show_line_dir()
    dif.show_direction_dif()
    dif.show_value_dif()

