import json
import pandas as pd

path = "./国民经济行业分类_2017.json"

with open(path, "r") as f:
    data = json.load(f)

df = pd.DataFrame(columns=["code", "name"])


def parse_name_code_then_append(data, dataframe):
    code = data["code"]
    name = data["name"]
    dataframe.loc[len(dataframe)] = [code, name]
    children = data["children"]
    return children


for d in data:
    children1 = parse_name_code_then_append(d, df)
    if len(children1) > 0:
        for c1 in children1:
            children2 = parse_name_code_then_append(c1, df)
            if len(children2) > 0:
                for c2 in children2:
                    children3 = parse_name_code_then_append(c2, df)
                    if len(children3) > 0:
                        for c3 in children3:
                            children4 = parse_name_code_then_append(c3, df)
                            pass
            pass
    pass

df.to_csv('./国民经济行业分类_2017.csv', index=False)

if __name__ == "__main__":
    pass
