prompt_template = """
    You are an expert at creating interview questions from a given text.
    Your goal is to prepare a list of questions that are likely to be asked in an interview for the given text. 
    You do this by first understanding the text and then creating a list of questions that are likely to be asked in an interview for the given text.

    Here is the text:
    ----------
    {text}
    ----------

    Create a list of 10 questions that are likely to be asked in an interview for the given text. Make sure to not loose any important details.

    QUESTIONS:
    """

refine_prompt_template = """
    You are an expert at creating interview questions from a given text.
    Your goal is to prepare a list of questions that are likely to be asked in an interview for the given text. 
    You do this by first understanding the text and then creating a list of questions that are likely to be asked in an interview for the given text.
    
    We have received some practice questions to a certain extent: {existing_answer}

    We have the option to refine the existing questions further or add new ones (only if necessary) with some more context below:

    ----------
    {text}
    ----------
    
    Given the new context, refine the original 10 questions in English. 
    If the context is not helpful, please provide the original questions.

    QUESTIONS:

    """
