from collections import deque

# Inspired by https://runestone.academy/runestone/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
def process_boolean_query(query_string):
    """ processes a boolean query from infix to postfix format for easier querying 
    
    The stack is implemented with a deque (more time efficient than a list).
    """
    precedence = {
        'AND_NOT' : 2,
        'AND' : 2,
        'OR_NOT' : 2,
        'OR' : 2,
        'NOT' : 2,
        '(' : 1,
        ')' : 0
    }

    # Getting the query tokens
    query_split = query_string.split(' ')
    query_tokens = []
    for token in query_split:
        if token[0] == '(' or token[-1] == ')':
            if token[0] == '(':
                while token[0] == '(':
                    query_tokens.append(token[0])
                    token = token[1:]
                query_tokens.append(token)
            else:
                close_brackets = []
                while token[-1] == ')':
                    close_brackets.append(token[-1])
                    token = token[:-1]
                query_tokens.append(token)
                for close_bracket in close_brackets:
                    query_tokens.append(close_bracket)
        else:
            query_tokens.append(token)

    # Composing the postfix version of the query
    operator_stack = deque()
    postfix_list = []
    for token in query_tokens:
        if token not in precedence.keys():
            postfix_list.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            top_token = operator_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = operator_stack.pop()
        else:
            while (operator_stack) and (precedence[operator_stack[-1]] >= precedence[token]):
                postfix_list.append(operator_stack.pop())
            operator_stack.append(token)

    while operator_stack:
        postfix_list.append(operator_stack.pop())
    
    return postfix_list

        

if __name__ == "__main__":
    print(process_boolean_query("(operating AND (system OR platform))"))
    print(process_boolean_query("(NOT test)"))