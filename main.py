import time
from selenium import webdriver

# used an api called selenium to access a web browser
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


# using this to access an api from Amazon
import boto3

# save my firefox profile so once the browser is laucnhed it will have me logged in and let me use autofill to make checking out fast

#USE THIS ONCE PC IS BACK
# profile = webdriver.FirefoxProfile(
#     r'C:\Users\Shanners\AppData\Roaming\Mozilla\Firefox\Profiles\n3ktxmv8.default-release')
# driver = webdriver.Firefox(profile)
driver = webdriver.Chrome('/Users/shaneclaycomb/Downloads/chromedriver')

# IMPORTANT
#LOOK HERE
#GIVE IT THE LINK TO THE PAGE WHEN YOU SEARCH RTX 3080 ON BEST BUY, IT WILL ADD THE FIRST THAT BECOMES AVAILABLE TO CART
driver.get(
    "https://www.bestbuy.com/site/searchpage.jsp?st=rtx+3080&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys")


#link to all 3080s
#https://www.bestbuy.com/site/searchpage.jsp?st=rtx+3080&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys


#3080 FE
#https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440


foundButton = False

cvv = "___"

try:  # while the item is not available to add to cart I contiuosly loop
    while not foundButton:
        addToCartButton = driver.find_element_by_class_name("add-to-cart-button")
        # if an item is not in stock in the code of the website page
        if ("btn-disabled" in addToCartButton.get_attribute("class")):
            # refresh the page every second to recheck
            time.sleep(1)
            driver.refresh()
        # once the item is in stock go through the checkout process
        else:
            # click the add to cart button
            addToCartButton.click()
            time.sleep(4)

            #I should have it text me as soon as it adds to cart in case it fails
            for i in range(5):
                print("here")
                client = boto3.client('sns', 'us-west-1')
                client.publish(PhoneNumber='+1 (xxx) xxx-xxxx', Message='the item has been purchased')

            # find the go to cart button had to use class name since different products all had different options for going to cart. this works for all of them
            goToCart = driver.find_element_by_class_name("go-to-cart-button")
            # again click and sleep
            goToCart.click()
            time.sleep(4)

            # selects the the option of shipping to your address
            ship = driver.find_element_by_xpath(
                "/html/body/div[1]/main/div/div[2]/div[1]/div/div/span/div/div[2]/div[1]/section[1]/div[4]/ul/li/section/div[2]/div[2]/form/div[2]/fieldset/div[2]/div[1]/div/div")
            ship.click()
            time.sleep(0.5)

            # find the go to checkout button and click it
            toCheckout = driver.find_element_by_xpath(
                "/html/body/div[1]/main/div/div[2]/div[1]/div/div/span/div/div[2]/div[1]/section[2]/div/div/div[3]/div/div[1]/button")
            # here is where the firefox profile is needed it, it will automatically sign you in after clicking this and fill your addess from your account
            toCheckout.click()
            time.sleep(5)

            # enter the cvv for the card I have save into the firefox browser
            enterCVV = driver.find_element_by_id("credit-card-cvv")
            enterCVV.send_keys(cvv)

            # and lastly hit the place the order button
            placeOrder = driver.find_element_by_xpath(
                "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/div/div[4]/div[3]/div/button")
            placeOrder.click()

            foundButton = True
# catch if the page timesout or if the webdriver can't find the element we are looking for
except TimeoutException or NoSuchElementException as exception:
    for i in range(5):
        print("here")
        client = boto3.client('sns', 'us-west-1')
        client.publish(PhoneNumber='+1 (xxx) xxx-xxxx', Message='the item has been purchased')
    pass


# using an amazon web service account I am using an API to send myself a text message once the item has been purchased
if foundButton:
    #spam myself to make sure I see it
    for i in range(5):
        print("here")
        client = boto3.client('sns', 'us-west-1')
        client.publish(PhoneNumber='+1 (xxx) xxx-xxxx', Message='the item has been purchased')