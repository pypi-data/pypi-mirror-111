class DummyClass:
    """Class to print input text

    Attributes:
    ------------
    text : string
    """
    
    def __init__(self, text):
        self.text = text

    def print_text(self):
        """prints input text
        
        Returns
        -------
        None
        
        """
        self.text = "*****************\n"+self.text+"\n*****************\n"
        print(self.text)
