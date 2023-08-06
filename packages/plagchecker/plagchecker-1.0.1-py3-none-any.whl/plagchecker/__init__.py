import requests
from requests.structures import CaseInsensitiveDict

class Checker:

    def __init__(self,apiKey) -> None:
        """
        Function defination:
        The function is used to initalize and accepts the parameters like APIKEY value which is available from www.prepostseo.com for free upto 200 searches for 5000 words.
        Note can be upgraded via premium plans
        """
        self.apiKey = apiKey
        # self.data = data
    
    def getDataLen(self,data) -> bool:
        """
        Function defination:
        The function is used to get the number of words from the data. If the number of words is less than or equal to 5000 returns True or else False.
        """
        if len(data)<=5000:
            return True
        return False


    def response(self,data):
        """
        Function defination:
        The function is used to get the response code. If status code is *200* means the execution was successful.
        """
        url = "https://www.prepostseo.com/apis/checkPlag"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        if(self.getDataLen(data)):
            data="key="+self.apiKey+"&data="+data
            self.resp = requests.post(url, headers=headers, data=data)
            self.res = self.resp.json()
            if(str(self.resp.status_code)=="200"):
                self.flag=1
                return str(self.resp.status_code), self.res
            else:
                self.flag=0
                return str(self.resp.status_code),""
        else:
            return "Number of words in the data exceeds the criteria defined of 5000 words.",""
    
    def getPlagPercent(self) -> str:
        """
        Function defination:
        The function is used to get the percentage of plagiarised content.
        """
        try:
            if self.flag==1:
                return str(self.res['plagPercent'])
        except:
            return "Error code: no parameter found with 'plagPercent' "
    
    def getUniquePrecent(self) -> str:
        """
        Function defination:
        The function is used to get the precentage of unique content
        """
        try:
            if self.flag==1:
                return str(self.res['uniquePercent'])
        except:
            return "Error code: no paramter found with 'uniquePercent' "

    def getSources(self) -> list:
        """
        Function defination:
        The function is used to get the sources from where the content was taken.
        """
        try:
            if self.flag==1:
                return self.res['sources']
        except:
            return "Error code: no parameter found with 'sources' "

    def getDetails(self) -> list:
        """
        Function defination:
        The function is used to get the additional details of individual querries in data.
        """
        try:
            if self.flag==1:
                return self.res['details']
        except:
            return "Error code: no parameter found with 'details' "