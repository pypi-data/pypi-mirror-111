# from __future__ import print_function
# from __future__ import absolute_import
# try:
#     from .configs.localConfigs import *
# except:
#     from .configs.sampleConfigs import *
# #from mAdvisor.bi.tests.testConfigs import *
#
# def get_test_configs(jobType,testFor = None):
#     print(jobType)
#     # from configs.localConfigs import *
#     # from mAdvisor.bi.tests.testConfigs import *
#     testConfigs = {
#         "story"        : get_story_config(),
#         "metaData"     : get_metadata_config(),
#         "training"     : get_training_config(),
#         "prediction"   : get_prediction_config(),
#         "subSetting"   : get_subsetting_config(),
#         "stockAdvisor" : get_stockadvisor_config()
#     }
#     # if jobType == "testCase":
#     #     if testFor == "chisquare":
#     #         testConfigs["testCase"] = get_chisquare_config()
#
#     return testConfigs[jobType]
