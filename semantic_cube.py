class semantic_cube():
    def __init__(self) -> None:
        self.sem_cube = {
            # ADD
            '+': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            # SUB
            '-': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            '*': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            '/': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            '<': {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            '>': {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            '==': {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            '<>': {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            'or': {
                'int': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'bool',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            'and': {
                'int': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'bool',
                    'text': 'ERR'
                },
                'text': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                }
            },
            '=': {
                'int': {
                    'int': 'bool',
                    'float': 'ERR',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'float': {
                    'int': 'ERR',
                    'float': 'bool',
                    'bool': 'ERR',
                    'text': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'bool',
                    'text': 'ERR'
                }
            }
        }

    def type_match(self, operator: str, operand1: str, operand2: str):
        return self.sem_cube[operator][operand1][operand2]
