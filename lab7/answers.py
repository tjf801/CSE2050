# Include your answers for this lab in the dictionary below.
# The keys of the dictionary are the pre-numbered algorithms.
# The values are your answers. Use:
#     'bubble'
#     'selction'
#     'insertion'
#     'merge'
#     'quick'

# #For instance, if you though all the algorithms  were bubble sort (they are not), this file should read:
# answers = {'alg_a': 'bubble',
#            'alg_b': 'bubble',
#            'alg_c': 'bubble',
#            'alg_d': 'bubble',
#            'alg_e': 'bubble'}

# Fill in your answers as the values in the dict below
answers = {
    'alg_a': 'selection', 
    'alg_b': 'quick',
    'alg_c': 'bubble', # bubble or insertion
    'alg_d': 'merge',
    'alg_e': 'insertion'  # bubble or insertion
}

valid_ans = {'bubble', 'selection', 'insertion', 'merge', 'quick'}
# Run this file in terminal to see if you used the correct formatting in your answer.
for k, v in answers.items():
    if v not in valid_ans:
        raise ValueError(f"Value '{v}' for key '{k}' is not in {valid_ans}")

print("Valid answer! Find out if it's right after the due date.")