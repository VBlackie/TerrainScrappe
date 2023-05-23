
# Terrains Scrapper (Puebla city)

This is a small demo of a web scrapper using Selenium to acquire data from a real estate website. It is custom made for "lands on sale" (meaning no houses, appartments, or anything similar, just pure dirt ground for sale) in the city of Puebla, Mexico.
The script will extract: price, area of land, location, zone, and city.

This small script includes some intentional errors and improvements that could be made to have a better experience and outcome. Several of those improvements are already documented below on this README. Check them out and see if you can implement them in your version of this code. ^^





## Libraries
Selenium.
As previously stated, this code uses Selenium as the default tool for webscrapping. This is also an example of a dyanamic webpage which will not upload all info in one take, but rather wait for user confirmation. Therefore, beautiful soup library will have it's limitations. This seemed like a prime example of when to use Selenium and hopefully it will prove useful for more than this webpage. Note that this version uses the service=Service(ChromeDriverManager().install()) and the webdriver on the drivers folder is no longer used. It was left there in case someone would like to use the old 'chromedriver.exe' method. Both work, but the formentioned one is the one recommended by the library itself.


Installing selenium: pip install selenium

Time and datetime.
In some occations on this code, time library is used to make a small interval for the webpage to load completly and also to avoid sending to many requests to the server and being banned because of it. Be mindful and kind with the server :). Instead of the time library you can also use WebDriverWait by Selenium, which will make the code more efficient.

Installing time: pip install time

Datetime library is used for a timestamp. This code generates a file with a timestamp so that later, the webpage could be scrapped again and ADD or REMOVE records accordingly.

Installing datetime: pip install datetime
## Code structure
The code structure follows the standard:
- Libraries
- Global variables
- Functions
- Main 

Libraries: Read the section above, but aside that there are some other libraries like pandas that are also installed. Nothing extraordinary.

Global variables:
url : This is the main page from where all webpages will be obtained. In case you want to change the city, or type of terrain to perform web scrapping, change this webpage to the one your main query will result. Examples: "https://www.inmuebles24.com/departamentos-en-renta-q-toluca.html", "https://www.inmuebles24.com/casas-en-venta-en-veracruz-provincia.html"

url2: This was just a testing variable, feel free to use it to debug in case you need another url.

all_terrains: This is where the data will be scrapped to from each posting card from the website. It starts as an empty list to keep adding records.

df_header: This is the structure we want on our output file

df_error: This is a list with only "Error" as an ouput. It's there for further debugging, but for time constraints, this is only included as a placeholder.

df: This will initialize the dataframe with the proper header. Could be added at the main file instead of the "variables zone" but since it could be renamed, this seemed ok at the time of creating the variable.

file_name_prefix: The output file will have a name that includes a timestamp, so it needs to be constructed with a couple of prefixes. Feel free to change it if you want your file to be named differently.

Functions:
Each function is very descriptive of what it does. Also it is written in order of apperance in the code for further references.

Main:
The main code wants to:
1. Open the webpage with Selenium.
2. Read the html code and find all postings, extract their data, and save it to a variable.
3. Append each record to the "all terrains" variable
4. Get the information to nex page to continue the web scrapping.
5. When we reach the end of all pages, then it will perform some cleaning on the data. It will remove unwanted info and just leave price, area, location, city, and zone.
6. Once the information is "clean", it will add each record to a pandas dataframe and then upload that as a csv file.

Note that here are some time.sleep(t) functions that only are there for the code to wait a random amount of seconds.



## Errors and improvements
This code is made as an example of usage for selenium and includes some areas that can be improved, but since this was made with some practices for students in mind, they were left here. Here are the most notorious ones:

--Web scrapping extraction and cleaning is flawed:
The main issue that you will find with this scrapper is that some posting cards (in code refered to as records) not all information has the same structure.
When using:
 terrain = driver.find_element(By.CLASS_NAME, 'postings-container')
 terrains = terrain.find_elements(By.XPATH, '//div[@data-qa="posting PROPERTY"]')

it returns the WHOLE record, but sometimes the posting card doesnt include "the zone", other times it will include a "up%" notifier which the webpage includes to promote such places, sometimes it includes double prices or price ranges. This messes up the logic in the "cleaning" function because it was only thought for the most repeated case in the posting cards. The cleaning function counts the line jumps and interprets that as field, but when there are more or less line jumps (\n)m the code will just either: be in an error of index out of range or just cram up everything as every line goes.

This is also the reason for the df_error list created prevoiusly, as it will indicate a placeholder for such mistakes and later on will be removed for the correct solution.

The correct way of solving this is instead of using the xpath for the entire posting card, would be to select the posting card, and inside the posting card check for the XPATH to each element. This means we need a specific variable for each data acquired:

price = terrain.find_element(By.XPATH, //div[@somevariable="price"])
location = terrain.find_element(By.XPATH, //div[@somevariable="location"])

This of course will make the code somewhat bigger, and the logic on cleaning will also need to include this new variables. But overall this guarantees that the information is there, and if it is not, then a TRY - EXCEPT will do the trick with EXCEPT do a default price = NA, location = NA.

--Open browser: When using selenium to navigate between pages, the webpages recognizes that who uses the webpage is not human and a captcha comes in place. There are ways to deal with the captcha, but a workaround was just to save the info for the next page and open a new webdriver. This is not the best workaround since the webpage can change page with only the script.
Furthermore, the same code is used twice on the Main function which implies it should be refered to as a function. This will improve readability.

--Clean record as lambda: the clean function uses a variable that is immediately replaced. This is within the usages of lambda expresions. Give it a try!

--Time.sleep : Time sleep is used to be gentle with the server and avoid saturating it and doing requests too fast. Also, it uses the random library to try not to look too much as a robot having intervals between two prime numbers. It should be replaced with WebDriver.Wait function instead, since it's way of waiting is more natural: It waits for the driver for a specific occurence to continue with the code.

--Pandas.dataframe performance: We are using right now dataframe and add each record as it is created. Is this best way of doing this? The way pandas like the information to be digested, would be better as a list of lists or record by record? The %%timeit funcion will give you a nice insight on what happens underneath pandas when doing this. It might be worth it to save all_terrains cleaned as a list of lists and append them to a dataframe and compare that to a record by record approach as we are doing right now. 

This are the main ways to imporve this code, feel free to add feedback or some awesome change that will improve either readability or performance!! Keep on coding ^^




## Documentation

[Documentation](https://linktodocumentation)

https://www.selenium.dev/documentation/webdriver/elements/information/

https://sparkbyexamples.com/pandas/pandas-dataframe-tutorial-beginners-guide/

https://selenium-python.readthedocs.io/locating-elements.html

https://www.pythonforbeginners.com/basics/python-list-manipulation


## FAQ

#### Can I use this code snippet with a diffent city/place?

Yes! In the section Code structure > Global variables > url you can change the "url" variable to the main webpage you are trying to scrappe (see Code Structure in the Readme for another url example). I have not tried all combinations but most seem to work fine.

#### This code doesn't work perfectly, I want a perfect database as output!!

Refer to Errors and imporvements tab in the Readme. This is a code that is used as a demo and is not thought to be production grade. Some mistakes where made because doing the correct solution takes a little more time than I wish I had for an example of "how to use selenium as an example".
This is no excuse and hopefully in the future this will improve drastically.Also it is done in spare time with love and attention, I will try to do better next time. 

However, most improvements are already addressed in the Errors and improvements tab. Feel free to send me some feedback on your take for this solution ^^.

### Why not use beautiful soup standalone or combined with Selenium?
Certainly it could be done! Using bs4 would work as well in conjuntion with Selenium is a powerful tool. Personally I was only trying to do a Selenium only example, and it was fun to see how far could it go.

### What about using fully fledged web scrappers, is it better than Selenium?
Recently I have come to like more and more such solutions to be honest! Dynamic webpages can sometimes be time consuming and stressful. Even worse, most web programmers dont like their sites to be scrapped and change the html tree every month or so. In those cases I think paid web scrappers could be a nice weapon in your arsenal. But so is Selenium for web scrapping. Immo If you can spare some time and do a script to scrappe for yourself that's awesome, plus it gives you experience in programming. Every tool has it's place.

### I think I have a better solution, can I share it with you or others?
YES!! Absolutely. The more feedback we get as a community the better. You might have thought of something I have not even thought about, or in reverse as well, but the idea is to keep on learning from each other.

### Can I use your code and share with other?
Yes! Just let them know where you got this from. Use it wisely ^^


