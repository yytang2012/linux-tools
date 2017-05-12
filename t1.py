import json

from misc import get_percentage


def print_result(one_day_dict):
    total_count = 0
    all_reduction_count = 0
    all_xuzhang = 0
    top = 50
    for idx in range(0, top):
        value_list = one_day_dict[str(idx)]
        value = value_list[0]

        names = [value[0] for value in value_list if value[0] != 'Not appear']
        print('{idx}: {name}'.format(idx=idx+1, name=names[0]))
    #     reduction_count = value[1]
    #     xuzhang = value[2]
    #     candidate_count = value[3]
    #     if total_count == 0:
    #         total_count = value[4]
    #     reduction_percent_candidate = get_percentage(reduction_count, candidate_count)
    #     reduction_percent_total = get_percentage(reduction_count, total_count)
    #     all_reduction_count += reduction_count
    #     all_xuzhang += xuzhang
    #     hit_ratio = value[5]
    #
    #     print('{0}-{1}: {2}, {3}, {4}, {5}. {6}'.format(
    #         idx, name, reduction_count, xuzhang, reduction_percent_candidate, reduction_percent_total, hit_ratio))
    # print("Top{0}: {0}, {2}, {3}, {4}".format(top,
    #                                           all_reduction_count, get_percentage(all_reduction_count, total_count),
    #                                           all_xuzhang, get_percentage(all_xuzhang, total_count)))

if __name__ == '__main__':
    dataset = None
    with open('/home/yytang/Documents/final-results/task1/dataset.txt', 'r') as f:
        # with open('/home/yytang/Documents/apps/task5/task5-dataset-6.txt', 'r') as f:
        dataset_string = f.read()
        dataset = json.loads(dataset_string)

    # for one_day_dict in dataset:
    #     print_result(one_day_dict)
    print_result(dataset[0])
