class semantic_cube():
    def __init__(self) -> None:
        self.sem_cube = {
            # ADD
            '+': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                }
            },
            # SUB
            '-': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                }
            },
            '*': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                }
            },
            '/': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                }
            },
            '<': {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                }
            },
            '>': {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                }
            },
            '==': {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                }
            },
            '<>': {
                'int': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                }
            },
            'or': {
                'int': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'bool'
                }
            },
            'and': {
                'int': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'bool'
                }
            },
            '=': {
                'int': {
                    'int': 'bool',
                    'float': 'ERR',
                    'bool': 'ERR'
                },
                'float': {
                    'int': 'ERR',
                    'float': 'bool',
                    'bool': 'ERR'
                },
                'bool': {
                    'int': 'ERR',
                    'float': 'ERR',
                    'bool': 'bool'
                }
            }
        }

    def type_match(self, operator: str, operand1: str, operand2: str):
        return self.sem_cube[operator][operand1][operand2]
