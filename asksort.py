from functools import total_ordering


@total_ordering
class Item:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        if (self.name, other.name) in comparison_memo:
            return comparison_memo[(self.name, other.name)]

        for intermediary in items:
            if intermediary == self or intermediary == other:
                continue
            if comparison_memo.get(
                (self.name, intermediary.name), False
            ) and comparison_memo.get((intermediary.name, other.name), False):
                comparison_memo[(self.name, other.name)] = True
                comparison_memo[(other.name, self.name)] = False
                return True  # self is better than other
            if not comparison_memo.get(
                (self.name, intermediary.name), True
            ) and not comparison_memo.get((intermediary.name, other.name), True):
                comparison_memo[(self.name, other.name)] = False
                comparison_memo[(other.name, self.name)] = True
                return False  # self is worse than other

        result = self.ask_user(other)
        comparison_memo[(self.name, other.name)] = result
        comparison_memo[(other.name, self.name)] = not result
        return result

    def ask_user(self, other):
        answer = (
            input(f"Is {self.name} better than {other.name}? (y/n): ").strip().lower()
        )
        return answer == "y"


comparison_memo = {}  # global memoization table

if __name__ == "__main__":
    method = (
        input("Enter 'paste' to paste items or 'file' to load from a file: ")
        .strip()
        .lower()
    )
    item_names = []

    if method == "paste":
        print("Enter the items, one per line. Enter an empty line when done:")
        while True:
            line = input()
            if line == "":
                break
            item_names.append(line.strip())
    elif method == "file":
        file_path = input("Enter the path to your text file: ").strip()
        try:
            with open(file_path, "r") as file:
                item_names = file.read().splitlines()
        except FileNotFoundError:
            print("File not found. Please check the path and try again.")
            exit()

    items = [Item(name) for name in item_names if name]  # Exclude empty lines

    items.sort()

    print("Sorted items based on your preferences:")
    for rank, item in enumerate(items, start=1):
        print(f"{rank}. {item.name}")
