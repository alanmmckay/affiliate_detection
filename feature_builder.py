from urllib.parse import urlparse

def build_parameter_list(parameter_dict):
    """
        A function which receives a dictionary whose keys describe a parameter
        of the set and returns a list of these parameters. This is used to
        ensure an enforced ordering as the paramters are built into feature
        sets
    """
    parameter_list = list()
    for parameter in parameter_dict:
        parameter_list.append(parameter)
    return parameter_list


def build_url_map(info_dict):
    """
        A function which receives a dictionary formed through a crawl (in the
        context of this project) and returns a dictionary whose keys are the
        urls contained in each pages' anchor tags. The values for these keys
        are the urls which contain the anchor tags. This is used to allow
        easy navigation through dictionary formed through the crawl.
    """
    url_map = dict()
    for hostname in info_dict:
        for url in info_dict[hostname]:
            for anchor in info_dict[hostname][url]['anchors']:
                url_map[anchor] = url #Should consider a log of duplicates
    return url_map


def build_value_map(info_dict):
    """
        A function which receives a dictionary formed through a crawl (in the
        context of this project) and returns a dictionary whose keys are the
        values of query string parameters discovered through the crawl. A
        value of this dictionary's key set is some unique value to act as an
        encoding.
    """
    current = 1
    value_map = dict()
    for hostname in info_dict:
        for url in info_dict[hostname]:
            anchors = info_dict[hostname][url]['anchors']
            for anchor in anchors:
                queries = info_dict[hostname][url]['anchors'][anchor]['queries']
                for query in queries:
                    key = queries[query]
                    try:
                        value_map[key]
                    except:
                        value_map[key] = current
                        current += 1
    return value_map


def build_row_dict(info_dict, parameter_list):
    """
        This function creates a dictionary such that each key is a URL from
        the initial crawl and the subsequent value list is that key's value
        for each parameter. This is currently being unused and needs to factor
        mapped values.
    """
    site_dict = dict()
    for hostname in info_dict:
        for url in info_dict[hostname]:
            anchors = info_dict[hostname][url]['anchors']
            for anchor in anchors:
                site_dict[anchor] = list()
                for parameter in parameter_list:
                    queries = anchors[anchor]['queries']
                    if parameter in queries:
                        site_dict[anchor].append(1)
                    else:
                        site_dict[anchor].append(0)
                if anchors[anchor]['annotation'] == 'yes':
                    site_dict[anchor].append(1)
                else:
                    site_dict[anchor].append(0)
    return site_dict


def build_col_dict(info_dict,parameter_list,url_map,value_map):
    """
        A function which produces a dictionary whose keys are some query-string
        paramter and the values are a list where each entry (i) of the list is
        representative of the value for entity (i). An entity is some url from
        gathered for this project to classify for affiliate status.
    """
    col_dict = dict()
    col_dict['training_website_name'] = list()
    col_dict['training_target'] = list()
    for url in url_map:
        col_dict['training_website_name'].append(url)
        origin = url_map[url]
        hostname = urlparse(origin).hostname
        isaffiliate = info_dict[hostname][origin]['anchors'][url]['annotation']
        if isaffiliate == 'yes':
            col_dict['training_target'].append(1)
        else:
            col_dict['training_target'].append(0)
    for parameter in parameter_list:
        col_dict[parameter] = list()
        for url in url_map:
            hostname = urlparse(url_map[url]).hostname
            queries = info_dict[hostname][url_map[url]]['anchors'][url]['queries']
            if parameter in queries:
                #col_dict[parameter].append(value_map[queries[parameter]])
                col_dict[parameter].append(1)
            else:
                col_dict[parameter].append(0)
    return col_dict

