"""
Author: William Wyatt
Email: william.wyatt@cgu.edu
Purpose: To order name comparisons.

DISCLAIMER: This is not a name parser.
"""

#Input: Dictionary, String or Name object
#Return: Name object
#Purpose: Casts some objects to Name objects.
def toName(obj):
    if issubclass(type(obj),dict):
        if 'name' in obj:
            return Name.parse(obj['name'])
        if 'firstName' in obj:
            return Name(obj['firstName'],obj['middleName'],obj['lastName'])
        else:
            return Name(obj['first'],obj['middle'],obj['last'])            
    elif issubclass(type(obj),str):
        return Name.parse(obj)
    elif issubclass(type(obj),bool):
        return obj
    else:
        raise Exception("Failed to parse object!",obj)


#Function decorator for toName function.
def nameify(func):
    def verify_name(*args,**kwargs):
        args = [arg if issubclass(type(arg),Name) else toName(arg) for arg in args]
        return func(*args,**kwargs)
    return verify_name


#Name Class
"""
The Name class can be initialized two ways:
myName = Name("Neil","D","Tyson") #Preferred
or
myName = Name("Neil",None,"Tyson") #Preferred
or
myName = Name.parse("Neil deGrasse Tyson")

If you use parse and your name has more than three components,
 it will be marked as difficult and will fail all comparisons.

Parse your names before giving it to the Name object.
"""
class Name:
    suffixes = ['JR','SR','MR','MS','I','II','III','IV','V','DE','LA','EL','SNR']
    """
    first: first name
    middle: middle name (If there is none give it empty string or None)
    last: last name
    difficult: If the name is complex & should not be compared
    original: The original string used in the class function Name.parse()
    """
    def __init__(self,first,middle,last,difficult=False,original=None,components=[]):
        self.components = components
        self.difficult = difficult #Boolean that makes it fail all comparisons
        self.original = original #Store the originally parsed string
        if difficult:
            self.first=first.upper()
            self.middle=[m.upper() for m in middle]
            self.last=last.upper()
        else:
            self.first = first.upper()
            if last is not None:
                self.last = last.upper()
            else:
                self.last = None
            if middle is None or middle=="" or middle=="None":
                self.middle = None
            else:
                self.middle = middle.upper()
        self._clean_suffix()

    def _clean_suffix(self):
        suffixes = ['JR','SR','MR','MS','I','II','III','IV','V','DE','LA','EL','SNR','DR','']
        if self.first is not None:
            pass
        

    """
    Discription: Really basic parser.
    Input: String of the form "Neil Tyson" or "Neil deGrasse Tyson"
    Output: Name object
    """
    def parse(string):
        difficult = False
        clean = lambda a: a.replace('.','').strip().upper()
        components = [clean(s) for s in string.split(' ') if clean(s) not in Name.suffixes]
        first=middle=last=None
        if len(components) == 1:
            first = components[0]
        elif len(components) == 3:
            first, middle, last = components
        elif len(components) == 2:
            first,last = components
            middle=None
        else:
            difficult = True
            first = components[0]
            last = components[-1]
            middle = components[1:-1]
        if middle=="": middle=None
        return Name(first,middle,last,difficult,original=string,components=components)

    #A difficult name is a parsed string with more than 2 components
    #Names are marked as difficult because parsing names is imperfect.
    #When a name if marked as difficult it automatically fails all comparisons
    def isDifficult(self):
        return self.difficult

    #Going to do all comparisons here.
    #Lower the score the better
    @nameify    
    def compare(self,name):
        #Match first & last name exactly
        if self.equal_primary(name):
            if self.middle is None:
                return 2 #No middle name given
            elif self.equal_middle_full(name):
                return 0 #Full middle names are equal
            elif self.equal_middle_full(name):
                return 0.5 #Middle component matched
            elif self.equal_middle_initial(name):
                return 1 #First char in middle names equal
            elif self.equal_middle_initial_component(name):
                return 1.5 #Middle initial matched
            return 3 #No middle name matched
        elif self.equal_first_name(name):
            return 3.5 #Only first name matched
        return 4 #Nothing matched

    @nameify
    def equal(self,name):
        if self.isDifficult() or name.isDifficult():
            return False
        first  = name.first  == self.first
        middle = name.middle == self.middle
        last   = name.last   == self.last
        return first and middle and last

    @nameify
    def equal_primary(self,name):
        difficult = self.isDifficult() or name.isDifficult()
        first = name.first==self.first
        last = name.last==self.last
        return first and last and not difficult

    @nameify
    def equal_middle_initial_component(self,name):
        if self.middle is None or isinstance(name.middle,list):
            return False
        for middle in self.middle:
            if middle[0] == self.middle[0]:
                return True
        return False
    
    @nameify
    def equal_middle_initial(self,name):
        if isinstance(name.middle,list): return False
        if self.middle is not None and name.middle is not None:
            return self.middle[0] == name.middle[0]
        else:
            #No Middle Name
            return False
    @nameify
    def equal_middle_full_component(self,name):
        if self.middle is None or isinstance(name.middle,list) or len(self.middle)==1:
            return False
        for middle in self.middle:
            if middle == self.middle:
                return True
        return False
    
    @nameify
    def equal_middle_full(self,name):
        if isinstance(name.middle,list): return False        
        if self.middle is not None and name.middle is not None:
            if len(self.middle) == 1:
                return False #Middle name is only an initial!
            return self.middle == name.middle
        else:
            #No Middle Name
            return False

    @nameify
    def equal_first_name(self,name):
        return self.first == name.first
    
    def __str__(self):
        if isinstance(self.middle,list):
            return f"{self.first} [{' '.join(self.middle)}] {self.last}"
        return f"{self.first} {self.middle} {self.last}"
    def __repr__(self):
        if isinstance(self.middle,list):
            return f"{self.first} [{' '.join(self.middle)}] {self.last}"
        return f"{self.first} {self.middle} {self.last}"    
