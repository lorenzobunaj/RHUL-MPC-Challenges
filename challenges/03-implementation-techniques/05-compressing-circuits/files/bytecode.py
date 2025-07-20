bytecode = [
    ("PUSH_CONST", 0), 
    ("STORE", "i"),
    ("LABEL", "LOOP_I"),
        ("LOAD", "i"),
        ("PUSH_CONST", 5),
        ("LTE",),    
        ("JMP_IF_FALSE", "END"),

        ("PUSH_CONST", 0), 
        ("STORE", "j"),
        ("LABEL", "LOOP_J"),
            ("LOAD", "j"),
            ("PUSH_CONST", 16),
            ("LT",),
            ("JMP_IF_FALSE", "INCREMENT_I"),

            ("LOAD_ACC",),  
            ("LOAD", "i"),
            ("LOAD", "j"),
            ("LOOKUP",),    
            ("XOR",),
            ("STORE_ACC",),   

            ("LOAD", "j"),
            ("INC",),
            ("STORE", "j"),
            ("JMP", "LOOP_J"),

        ("LABEL", "INCREMENT_I"),
        ("LOAD", "i"),
        ("INC",),
        ("STORE", "i"),
        ("JMP", "LOOP_I"),

    ("LABEL", "END"),
    ("RETURN",)
]