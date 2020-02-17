# Import libraries
from collections import deque

# Import local files
from db_operations import retrieve_courses_doc_ids_not_from_set, retrieve_courses_doc_ids_from_term

# execute_boolean_query inspired by https://runestone.academy/runestone/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
# TODO move a lot of the set theory directly to sql commands, most likely more efficient on a large data set
def execute_boolean_query(postfix_query_tokens):
    """ Get list doc_id's of all documents that are accpeted by the query """
    operators = ['AND', 'AND_NOT', 'OR', 'OR_NOT', 'NOT']
    operand_sets = deque()
    for token in postfix_query_tokens:
        if token not in operators:
            operand_sets.append(retrieve_courses_doc_ids_from_term(token)) # Add the current set of id's to the stack
        elif token == 'NOT':
            operand_set_1 = operand_sets.pop()
            operand_sets.append(retrieve_courses_doc_ids_not_from_set(operand_set_1))
        else:
            operand_set_2 = operand_sets.pop()
            operand_set_1 = operand_sets.pop()
            if token == 'AND':
                operand_sets.append(intersection(operand_set_1, operand_set_2))
            elif token == 'AND_NOT':
                operand_sets.append(intersection(operand_set_1, retrieve_courses_doc_ids_not_from_set(operand_set_2)))
            elif token == 'OR':
                operand_sets.append(union(operand_set_1, operand_set_2))
            elif token == 'OR_NOT':
                operand_sets.append(union(operand_set_1, retrieve_courses_doc_ids_not_from_set(operand_set_2)))
            else: # unrechable case
                None
    return operand_sets.pop()


def union(lst1, lst2):
    return list(set(lst1) | set(lst2))

def difference(lst1, lst2):
    return [item for item in lst1 if item not in set(lst2)]

def intersection(lst1, lst2):
    return [value for value in lst1 if value in set(lst2)]

if __name__ == "__main__":
    print(execute_boolean_query(['&', '/', 'OR']))
    print(execute_boolean_query(['2174', '3', 'AND']))
