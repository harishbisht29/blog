from bs4 import BeautifulSoup
import re
html= '''
<div>
<p>emoji:lol</p>
</div>
'''

class AutoStyles:

    def clean(self, content):
        # Clean paragraphs for different senarios. This is done to keep html structure safe.
        # 1. New line styling <p>{{{style_name}}}</p> -> {{{style_name}}}
        pattern= '<p>(\{\{\{.*\}\}\})</p>'
        new_pattern= r'\1'
        content= re.sub(pattern, new_pattern, content)
        # 2. Inline styling
        pattern= '<p>(\{\{\{.*\}\}\})'
        new_pattern= r'\1'
        content= re.sub(pattern, new_pattern, content)

        #Replace {{{end}}} -> </span>
        content= content.replace("{{{end}}}","</span>")

        # Build the start of span tag. Replace {{{style_name}}} -> <span class="style_name"> 
        pattern= '\{\{\{(.*)\}\}\}'
        new_pattern= r'<span class="\1">'
        content= re.sub(pattern, new_pattern, content)
         
        return content

    def __init__(self, content):
        cleaned_content= self.clean(content)
        #customization for emojis 
        emoji_encodings= {
            ':)':"&#x1F642;",
            ":(":"&#x1F641;",
            ".^_":"&#x1F928;",
            "**)":"&#x1F929;",
            ":|":"&#x1F610;",
            "emoji:tired":"&#x1F62B;",
            "emoji:sleepy":"&#x1F62A;",
            "emoji:money":"&#x1F911;",
            ";)":"&#x1F609;",
            "emoji:wave":"&#x1F44B",
            "emoji:namaste":"&#x1F64F",
            "emoji:lol":"&#x1F604"

        }
        for k,v in emoji_encodings.items():
            cleaned_content= cleaned_content.replace(k,v,100)
        self.soup= BeautifulSoup(cleaned_content,'html.parser')
    
    def tocCustomize(self,base_tag):
        # print("------------Customizing\n",base_tag)
        l_items= base_tag.findAll('li')
        # Linking a tags for all the list items inside "toc" class
        # for all n lis inside toc class create links from toc_item1- toc_itemn
        for i in range(len(l_items)):
            a= self.soup.new_tag("a")
            a.string= l_items[i].get_text()
            a['href']= '#toc_item'+str(i+1)
            l_items[i].string= ''
            l_items[i].append(a)

        # Assigning ids to all the h4 tags in content
        # All the h4 tags will be assigned id sequentially
        heading_tags= self.soup.findAll('h4')
        for i in range(len(heading_tags)):
            heading_tags[i]['id']= 'toc_item'+str(i+1)
        # print("--------------After customizing\n",self.soup)

    def customize(self):
        # add search condition
        # toc
        toc_tags= self.soup.findAll("span", {"class": "toc"})
        for t in toc_tags:
            self.tocCustomize(t)
        

    def getStyledContent(self):
        self.customize()
        return (str(self.soup))

if __name__ == '__main__':
    a= AutoStyles(html).getStyledContent()
    print(a)
