from bs4 import BeautifulSoup
import re
html= '''
<div>
<p>{{{toc}}}</p>
<p>Hello World</p>
<ul>
<li>Hi</li>
<li>there</li>
<li>How</li>
</ul>
<p>{{{end}}}</p>
<p>{{{highlight}}}Hello World {{{end}}}</p>
<p><h4>Hello</h4></p>
<p><h4>How</h4></p>
<p><h4>Are</h4></p>
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
        pass

    def getStyledContent(self):
        self.customize()
        return (str(self.soup))

if __name__ == '__main__':
    a= AutoStyles(html).getStyledContent()
    print(a)
