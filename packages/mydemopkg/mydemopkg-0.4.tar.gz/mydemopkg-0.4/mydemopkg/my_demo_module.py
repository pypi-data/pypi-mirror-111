class DummyClass:
    """Class to print input text

    Attributes:
    ------------
    text : string
    """
    
    def __init__(self, text):
        self.text = text

    def print_text(self):
        """prints input text in lower case
        
        Returns
        -------
        None
        
        """

        # convert string to lower case
        self._text_lower()
        #print(self.text)
        # print
        self.text = "*****************\n"+self.text+"\n*****************\n"
        print(self.text)

    def _text_lower(self):
        """prints input text in lower case

        Returns
        -------
        None

        """
        self.text = self.text.lower()

