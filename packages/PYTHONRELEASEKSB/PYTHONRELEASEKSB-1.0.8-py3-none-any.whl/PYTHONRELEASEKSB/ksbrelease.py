import requests
import pandas

def ksbAddNum(a,b):
    return a+b;


def getVariantsOfGene(gene_id){
    # response = requests.get('http://korsair.kisti.re.kr/api/gene/' + gene_id)
    # result = response.json()
    # df = pandas.read_json(result, orient='index')
    # print(df)
    rs = requests.get('https://www.google.co.kr')
    print(rs)
}