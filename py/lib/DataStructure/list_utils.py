def get_counts(items: list) -> dict:
    counts = {}
    for item in items:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts

def insert(items: list, idx: int, val: any) -> list:
    return items[:idx] + [val] + items[idx:]

def remove_duplicates(items: list) -> list:
    return list(get_counts(items).keys())

def load(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return [
            item.strip()
            for item
            in f.readlines()
            if item.strip() != ""
        ]

def drop(original_list, idx):
    copy_list = original_list.copy()
    copy_list.remove(copy_list[idx])
    return copy_list

def partition(items: list, split_condition: callable, modified_value: callable = None):
    partitions = {}
    for item in items:
        result = split_condition(item)
        if modified_value is not None:
            item = modified_value(item)
        if result in partitions:
            partitions[result].append(item)
        else:
            partitions[result] = [item]
    return partitions

def main():
    # items = load(f"")
    # print(len(items))
    # items = remove_duplicates(items)
    # print(len(items))
    pass

if __name__ == "__main__":
    main()
