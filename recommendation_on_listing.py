from operator import index
import pandas as pd

class recommendByListing():
    def create_leaf(self,r_df):
        r_df=r_df.sort_values("Rank",ascending=False)
        r_df.query("Type=='Leaf'").to_excel("Result/Recommendation_on_Listing_Leaf.xlsx",index=False)

    def create_vertical(self,df,r_df):
        l=[df["Leaf"][0]]
        dict={df["Vertical"][0]:l}
        # print(dict)
        for i in range(0,(len(df.index)-1)):
            
            if(df["Vertical"][i]==df["Vertical"][i+1]):
                dict[df["Vertical"][i+1]].append(df["Leaf"][i+1])
            else:
                l=[df["Leaf"][i+1]]
                d={df["Vertical"][i+1]:l}
                dict.update(d)


        # l1=[df["Leaf"][0]]
        # dict1={df["Middle"][0]:l}

        # for i in range(0,(len(df.index)-1)):
            
        #     if(df["Middle"][i]==df["Middle"][i+1]):
        #         dict1[df["Middle"][i+1]].append(df["Leaf"][i+1])
        #     else:
        #         l1=[df["Leaf"][i+1]]
        #         d1={df["Middle"][i+1]:l1}
        #         dict1.update(d1)
        # print(dict1)



        new_df = pd.DataFrame(columns=['Parent','Child','Cid','Count','Perc. of count'])
        for i in r_df.index:
            if(r_df["Type"][i]=="Vertical"):
                try:
                    key=r_df["clabel"][i]
                
                    for j in range (i+1,len(r_df.index)):
                        if(dict[key].count(r_df["clabel"][j])>0):
                            new_df.loc[len(new_df.index)] = [key,r_df["clabel"][j],r_df["cid"][j],r_df["count"][j],(100*r_df["count"][j]/r_df["count"][i])]
                except:
                    continue
                    
            # if(r_df["Type"][i]=="Middle"):
            #     try:
            #         key=r_df["clabel"][i]
                
            #         for j in range (i+1,len(r_df.index)):
            #             if(dict[key].count(r_df["clabel"][j])>0):
            #                 new_df.loc[len(new_df.index)] = [key,r_df["clabel"][j],r_df["cid"][j],r_df["count"][j],(100*r_df["count"][j]/r_df["count"][i])]
            #     except:
            #         continue


        # Getting leaf index after 5 of each vector 
        li=[]    
        c=1
        for i in range(0,len(new_df.index)-1):
            if(new_df["Parent"][i]==new_df["Parent"][i+1]):
                if(c>4):
                    li.append(i)
                else:
                    c+=1
            else:
                c=0
        #Removing leaf after 5 elements
        for i in li:
            new_df.drop([i],inplace=True)
        new_df.to_excel("Result/Recommendation_on_Listing_Vertical.xlsx",index=False)    
        
  

df=pd.read_excel("Modified_category.xlsx")
r_df=pd.read_excel("C_rank.xlsx")
a=recommendByListing()
a.create_leaf(r_df)
a.create_vertical(df,r_df)