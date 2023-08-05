import random
from pathlib import Path

random.seed(1)

_newsgroup_explanation_urls = {'electronics': 'https://github.com/SinaMohseni/ML-Interpretability-Evaluation-Benchmark'
                                              '/tree/master/Text/20news_group/human_attention/sci.electronics',
                               'med': 'https://github.com/SinaMohseni/ML-Interpretability-Evaluation-Benchmark/tree'
                                      '/master/Text/20news_group/human_attention/sci.med'}

_newsgroup_data_urls = {'electronics': 'https://github.com/SinaMohseni/ML-Interpretability-Evaluation-Benchmark'
                                       '/tree/master/Text/20news_group/org_documents/20news-bydate/20news-bydate-test/'
                                       'sci.electronics',
                        'med': 'https://github.com/SinaMohseni/ML-Interpretability-Evaluation-Benchmark/tree/master/'
                               'Text/20news_group/org_documents/20news-bydate/20news-bydate-test/sci.med'}

_newsgroupElecNames = ['53994', '53993', '53992', '53995', '53968', '54009', '54036', '54031', '54038', '54007',
                       '54000', '54053', '54065', '54062', '54001', '54039', '54006', '54030', '54008', '54037',
                       '54063', '54064', '54052', '54055', '54048', '54083', '54077', '54070', '54084', '54079',
                       '54046', '54041', '54015', '54012', '54024', '54023', '54040', '54078', '54047', '54085',
                       '54071', '54049', '54076', '54082', '54022', '54025', '54013', '54014', '53986', '53972',
                       '53981', '53988', '53989', '53999', '53990', '53997', '53991', '53998', '54050', '54057',
                       '54068', '54061', '54066', '54032', '54035', '54003', '54004', '54067', '54058', '54060',
                       '54056', '54069', '54051', '54005', '54002', '54034', '54033', '54011', '54016', '54029',
                       '54020', '54027', '54018', '54073', '54080', '54074', '54042', '54045', '54019', '54021',
                       '54017', '54028', '54010', '54044', '54043', '54075', '54081', '54072', '53984', '53983']

# some indexes from this list do not contain explanations in the github repo (12 of them). They have been manually
#   removed
_newsgroupMedNames = ['59263', '59297', '59290', '59264', '59252', '59299', '59255', '59237', '59254', '59253', '59298',
                      '59291', '59296', '59262', '59236', '59231', '59238', '59310', '59328', '59317', '59321', '59319',
                      '59326', '59318', '59327', '59320', '59329', '59316', '59311', '59305',
                      '59304', '59303', '59332', '59225', '59247', '59271', '59285', '59249', '59282',
                      '59276', '59248', '59277', '59283', '59284', '59270', '59279', '59246', '59241', '59234',
                      '59267', '59258', '59260', '59294', '59256', '59269', '59251', '59257', '59268', '59295', '59261',
                      '59259', '59314', '59313', '59325', '59322', '59323', '59324', '59312', '59315',
                      '59308', '59330', '59301', '59307', '59331', '59309', '59288', '59243',
                      '59281', '59275', '59272', '59287', '59273', '59274', '59280', '59289', '59242', '59245',
                      '59229']

_newsgroupAll = _newsgroupElecNames + _newsgroupMedNames
_newsgroupLabels = [0 for _ in range(len(_newsgroupElecNames))] + [1 for _ in range(len(_newsgroupMedNames))]

__temp = list(zip(_newsgroupAll, _newsgroupLabels))
random.shuffle(__temp)
_newsgroupAll, _newsgroupLabels = zip(*__temp)

_newsgroupNEntries = len(_newsgroupAll)
_newsgroupIndexes = {i: _newsgroupAll[i] for i in range(_newsgroupNEntries)}
_newsgroupLabels = {i: _newsgroupLabels[i] for i in range(_newsgroupNEntries)}

_newsgroupRoot = Path(__file__).parent.parent.absolute() / 'text/newsgroup/'
