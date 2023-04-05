from itertools import combinations_with_replacement

from BET import find_solutions


def answer_questions() -> tuple[
    tuple[tuple[str, ...], int],
    float,
    float
]:
    """Answer the extra flex questions.
    
    A few extra questions that are not for credit, but could be fun to figure out:
    * What is the best hand you can find, and how many solutions does it produce?
    * What percentage of hands have 0 solutions?
    * What percentage of hands have exactly 1 solution?

    Returns
    -------
        A tuple containing:
        1. A tuple with the best hand, and how many solutions it produces
        2. The percentage of hands with 0 solutions, as a float
        3. The percentage of hands with exactly 1 solution, as a float

    Addendum
    --------
    After running this function, which took around 3 minutes on my computer, I found:
    * the best hand is ('A', '4', '8', 'Q'), with 335 solutions
    * the probability of no solutions is 25.16%
    * the probability of exactly one solution is 0.879%
    """
    valid_cards = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    
    cards_by_num_solutions: dict[int, list[tuple[str, ...]]] = {}
    
    for cards in combinations_with_replacement(valid_cards, 4):
        print(f'Checking {cards}...', end='\r')
        num_solutions = sum(1 for _ in find_solutions(cards))
        if num_solutions not in cards_by_num_solutions:
            cards_by_num_solutions[num_solutions] = []
        cards_by_num_solutions[num_solutions].append(cards)
    
    max_num_solutions = max(cards_by_num_solutions)
    num_zero_solution = len(cards_by_num_solutions[0])
    num_one_solution = len(cards_by_num_solutions[1])
    total_solutions = sum(len(cards) for cards in cards_by_num_solutions.values())
    
    return (
        (cards_by_num_solutions[max_num_solutions][0], max_num_solutions),
        num_zero_solution / total_solutions,
        num_one_solution / total_solutions
    )

def main() -> None:
    (cards, max_sols), zero_prob, one_prob = answer_questions()
    print(f'Cards with most solutions: {cards}, with {max_sols} solutions')
    print(f'Probability of no solutions: {zero_prob}')
    print(f'Probability of one solution: {one_prob}')

if __name__ == '__main__':
    main()
