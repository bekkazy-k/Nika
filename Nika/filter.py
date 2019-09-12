# Filters to array
def filter_by_field_arr(json_data, field, value):
    output_included_json = [x for x in json_data if x[field] == value]
    output_excluded_json = [x for x in json_data if x[field] != value]
    return output_included_json, output_excluded_json


def filter_by_fields_arr(json_data, field, values):
    output_included_json = list()
    output_excluded_json = json_data
    for i in values:
        inc, output_excluded_json = filter_by_field_arr(output_excluded_json, field, i)
        for j in inc:
            output_included_json.append(j)
    return output_included_json, output_excluded_json


# Filters to single JSON
def filter_by_field_json(json_data, field, value):
    if json_data[field] == value:
        return True
    return False


def filter_by_fields_json(json_data, field, values):
    for i in values:
        if filter_by_field_json(json_data, field, i):
            return True
    return False


def exclude_by_field_json(json_data, field, value):
    if json_data[field] != value:
        return True
    return False


def filter_if_field_in_arr(json_data, field, value):
    if json_data[field] in value:
        return True
    return False
