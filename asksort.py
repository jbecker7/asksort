from functools import total_ordering
import argparse


@total_ordering
class Item:
    def __init__(self, name, comparison_memo):
        self.name = name
        self.comparison_memo = comparison_memo

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        comparison = self.comparison_memo.get_comparison(self.name, other.name)
        if comparison is not None:
            return comparison

        result = self.ask_user(other)
        self.comparison_memo.set_comparison(self.name, other.name, result)
        return result

    def ask_user(self, other):
        answer = (
            input(f"Is {self.name} better than {other.name}? (y/n): ").strip().lower()
        )
        return answer == "y"


class ComparisonMemo:
    def __init__(self):
        self.memo = {}
        self.items = {}

    def add_item(self, item):
        self.items[item.name] = item

    def get_comparison(self, name1, name2):
        # Check direct comparison
        comparison = self.memo.get((name1, name2))
        if comparison is not None:
            return comparison
        # Check inverse comparison
        if (name2, name1) in self.memo:
            return not self.memo[(name2, name1)]
        # Transitivity and inference logic to be handled after user input
        return None

    def set_comparison(self, name1, name2, result):
        # Set direct comparison
        self.memo[(name1, name2)] = result
        self.memo[(name2, name1)] = not result
        # Extend the memoization table with transitive relations
        self.update_transitive_relations(name1, name2, result)

    # This one I am not sure about yet, but it's a start
    def update_transitive_relations(self, name1, name2, result):
        for intermediary_name in self.items:
            # If intermediary_name can be used to infer new comparisons, update the memo
            if (name1, intermediary_name) in self.memo:
                # If name1 < intermediary_name and intermediary_name < name2, then name1 < name2
                if self.memo[(name1, intermediary_name)] == result:
                    self.memo[(intermediary_name, name2)] = result
                    self.memo[(name2, intermediary_name)] = not result
            if (intermediary_name, name2) in self.memo:
                if self.memo[(intermediary_name, name2)] == result:
                    self.memo[(name1, intermediary_name)] = result
                    self.memo[(intermediary_name, name1)] = not result


if __name__ == "__main__":
    # Hopefully this is the convention, idk for sure but seems file is the option you would want refactored as an arg? not pasting
    parser = argparse.ArgumentParser(
        description="Sort items based on user preferences with minimal comparisons."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to a text file containing items to sort, one per line.",
    )
    args = parser.parse_args()

    comparison_memo = ComparisonMemo()
    item_names = []

    if args.file:
        try:
            with open(args.file, "r") as file:
                item_names = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"File not found: {args.file}. Please check the path and try again.")
            exit()
    else:
        print("Enter the items, one per line. Enter an empty line when done:")
        while True:
            line = input()
            if line == "":
                break
            item_names.append(line.strip())

    items = [Item(name, comparison_memo) for name in item_names]
    for item in items:
        comparison_memo.add_item(
            item
        )  # Update comparison_memo with items, stored inside the object

    items.sort()

    print("Sorted items based on your preferences:")
    for rank, item in enumerate(items, start=1):
        print(f"{rank}. {item.name}")
