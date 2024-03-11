from functools import total_ordering
import argparse


@total_ordering
class Item:
    def __init__(self, name, comparison_memo):
        self.name = name
        self.comparison_memo = comparison_memo

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        comparison = self.comparison_memo.get_comparison(self.name, other.name)
        if comparison is not None:
            return comparison

        result = self.ask_user(other)
        self.comparison_memo.set_comparison(self.name, other.name, result)
        return result

    def ask_user(self, other):
        self.comparison_memo.increment_comparison_count()
        answer = (
            input(f"Is {self.name} better than {other.name}? (y/n): ").strip().lower()
        )
        return answer == "y"


class ComparisonMemo:
    def __init__(self):
        self.memo = {}
        self.items = {}
        self.comparison_count = 0

    def add_item(self, item):
        self.items[item.name] = item

    def get_comparison(self, name1, name2):
        return self.memo.get((name1, name2))

    def increment_comparison_count(self):
        self.comparison_count += 1

    def set_comparison(self, name1, name2, result):
        # Set direct comparison
        self.memo[(name1, name2)] = result
        self.memo[(name2, name1)] = not result
        # Extend the memoization table with transitive relations
        self.update_transitive_relations(name1, name2, result)

    # A different approach but still a wrong one :)
    def update_transitive_relations(self, name1, name2, result):
        # Iterate over all items to check possible transitive relations
        for intermediary_name in self.items:
            if intermediary_name == name1 or intermediary_name == name2:
                continue  # Skip if intermediary is one of the compared items (no transitive relation to update)

            forward_key = (name2, intermediary_name)
            backward_key = (intermediary_name, name1)

            # If A < B and B < C, then A < C
            if result and forward_key in self.memo and self.memo[forward_key]:
                self.set_direct_comparison(name1, intermediary_name, True)

            # If A > B and B > C, then A > C
            if result and backward_key in self.memo and self.memo[backward_key]:
                self.set_direct_comparison(intermediary_name, name2, True)

    def set_direct_comparison(self, name1, name2, result):
        self.memo[(name1, name2)] = result
        self.memo[(name2, name1)] = not result


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
        item_names = []
        while line := input():
            item_names.append(line.strip())

    items = [Item(name, comparison_memo) for name in item_names]
    for item in items:
        comparison_memo.add_item(
            item
        )  # Update comparison_memo with items, stored inside the object

    items.sort()

    print(f"Total comparisons made: {comparison_memo.comparison_count}")

    print("Sorted items based on your preferences:")
    for rank, item in enumerate(items, start=1):
        print(f"{rank}. {item.name}")
