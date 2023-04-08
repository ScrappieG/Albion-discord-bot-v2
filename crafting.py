
import random
import requests

#This page is a work in progress, im still finding a way to calculate the cost of crafting and fame.

TIER_LIST = {4:'T4_',5: 'T5_', 6: 'T6_', 7: 'T7_', 8:'T8_' }

#--------------------------
METAL_BAR = 'METALBAR'
CLOTH = 'CLOTH'
PLANK = 'PLANK'
#--------------------------
SOLDIER_ARMOR = 'ARMOR_PLATE_SET1'
KNIGHT_ARMOR = 'ARMOR_PLATE_SET2'
GUARDIAN_ARMOR = 'ARMOR_PLATE_SET3'
#---------------------------

#---------------------------
SCHOLAR_SANDALS = 'SHOES_CLOTH_SET1'
MAGE_SANDALS = 'SHOES_CLOTH_SET3'
CLERIC_SANDALS = 'SHOES_CLOTH_SET2'
#---------------------------

#---------------------------
LIGHT_CROSS_BOW = 'MAIN_1HCROSSBOW'
CROSSBOW = 'MAIN_2HCROSSBOW'
SIEGE_CROSSBOW = '2H_CROSSBOWLARGE'
#---------------------------

def get_prices(itemList, qualities=0, locations='Bridgewatch'):

    format = '.json'
    print(itemList)
    payload = {'locations': locations, 'qualities': qualities}
    url = f'https://www.albion-online-data.com/api/v2/stats/Prices/{itemList}{format}'
    response = requests.get(url, params=payload)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        print(response.status_code)
        return False

RETURN_RATE = .295


ARMOR_CRAFTING_FEE = 172 #per item

CROSSBOW_CRAFTING_FEE = 258 #per item

SANDAL_CRAFTING_FEE = 80 #per item

SETUP_FEE =.025 #2.5% setup fee

SALES_TAX=.04 #4% with premium

#-------------------------------------


ARMOR_FAME = 1440

SANDALS_FAME = 720

CROSSBOW_FAME = 2160

BOOK_TOTAL_FAME = 7200

#quality relys on a d1000 dice roll where every 60 quality spec 
#points you will get another dice to roll


def main_crafter(first_name, Last_name, item_tier, material_1, material_2, return_rate = None):

    if return_rate == None:
        return_rate = RETURN_RATE
    else:
        return_rate = return_rate/100

    item_info = craft(first_name=first_name,last_name=Last_name,item_tier=item_tier,material_1=material_1,material_2=material_2, return_rate=return_rate)
    return item_info




def craft(first_name,item_tier, last_name, material_1, material_2, return_rate = None):


    crafted_list = []
    tier = TIER_LIST[item_tier]
    fees = 0
    items = 0
    BM_price = 0
    fame = 0
    mat_cost_1 = 0
    mat_cost_2 = 0
    if last_name == 'armor':
        if first_name == 'knight':
            item = tier + KNIGHT_ARMOR
        elif first_name == 'soldier':
            item = tier + SOLDIER_ARMOR
        elif first_name == 'guardian':
            item = tier + GUARDIAN_ARMOR
        else:
            return 1

        item_price = get_prices(itemList=item,locations='Black Market')
        craft_cost_1 = 16
        craft_cost_2 = 0
        craft_fee = ARMOR_CRAFTING_FEE
        temp_price_of_bar = get_prices(itemList=(tier+METAL_BAR), locations='Bridgewatch')
        print(temp_price_of_bar)
        for i in range(len(temp_price_of_bar)):
            if temp_price_of_bar[i]['sell_price_min'] != 0:
                price_of_bar = temp_price_of_bar[i]['sell_price_min']
                break
            else:
                price_of_bar = 0
        mat_cost_1 = price_of_bar*material_1
        

    elif last_name == 'sandals':
        if first_name == 'mage':
            item = tier + MAGE_SANDALS
        elif first_name == 'scholar':
            item = tier + SCHOLAR_SANDALS
        elif first_name == 'cleric':
            item = tier + CLERIC_SANDALS
        else:
            return 1
        item_price = get_prices(itemList=item,locations='Black Market')
        craft_cost_1 = 8
        craft_cost_2 = 0
        craft_fee = SANDAL_CRAFTING_FEE
        temp_price_of_cloth = get_prices(itemList=(tier + CLOTH), locations='Bridgewatch')
        for i in range(len(temp_price_of_cloth)):
            if temp_price_of_cloth[i]['sell_price_min'] != 0:
                price_of_cloth = temp_price_of_cloth[i]['sell_price_min']
                break
            else:
                price_of_cloth = 0

        mat_cost_1 = price_of_cloth*material_1

    elif last_name =='crossbow':
        if first_name == 'light':
            item = tier + LIGHT_CROSS_BOW
            craft_cost_1 = 8
            craft_cost_2 = 16
        elif first_name == '2h':
            item = tier + CROSSBOW
            craft_cost_1 = 12
            craft_cost_2 = 20
        elif first_name == 'siege':
            item = tier + SIEGE_CROSSBOW
            craft_cost_1 = 12
            craft_cost_2 = 20
        item_price = get_prices(itemList=item,locations='Black Market')
        temp_price_of_bar = get_prices(itemList=(tier + METAL_BAR), locations='Bridgewatch')
        temp_price_of_plank = get_prices(itemList=(tier + PLANK),locations='Bridgewatch')
        price_of_bar = 0
        price_of_plank =0
        for i in range(len(temp_price_of_bar)):
            if temp_price_of_bar[i]['sell_price_min'] != 0:
                price_of_bar = temp_price_of_bar[i]['sell_price_min']
                break
            else:
                price_of_cloth = 0
        for i in range(len(temp_price_of_plank)):
            if temp_price_of_plank[i]['sell_price_min'] != 0:
                price_of_plank = temp_price_of_plank[i]['sell_price_min']
                break
            else:
                price_of_plank = 0

        craft_fee = CROSSBOW_CRAFTING_FEE
        mat_cost_1 = price_of_bar *material_1
        mat_cost_2 = price_of_plank *material_2
        
    else:
        print('error')
        return 1
    price = 0
    for i in range(len(item_price)):
        if item_price[i]['sell_price_min'] != 0:
            price = item_price[i]['sell_price_min']
            break
    print(item)

    while material_1 >= craft_cost_1 and material_2 >= craft_cost_2:

        temp_mat_1 = int(material_1 * return_rate)
        temp_mat_2 = int(material_2 * return_rate)

        while material_1 >= craft_cost_1 and material_2 >= craft_cost_2:

            material_1 = material_1 - craft_cost_1
            material_2 = material_2 - craft_cost_2

            BM_price = BM_price + price
            print(price)
            print(BM_price)
            fame_unit = get_fame(item=last_name)
            fame = fame + fame_unit
            items +=1
            fees = fees + craft_fee

        material_1 = temp_mat_1
        material_2 = temp_mat_2

    number_books = fame/BOOK_TOTAL_FAME
    set_up_fee = BM_price * SETUP_FEE
    sales_fee = BM_price * SALES_TAX
    total_mat_cost = (mat_cost_1) + (mat_cost_2)
    profit = BM_price - (sales_fee + set_up_fee + total_mat_cost)
    #roi = (profit / ((total_mat_cost + sales_fee + set_up_fee) * 100)

    roi = 1
    
    print(crafted_list)
    final_dict = {'profit': profit,'books_filled':number_books,'roi': roi, 'BM price': BM_price,'cost_of_material': total_mat_cost, 'fees': fees, 'items': items, 'item_list': crafted_list}
    
    return final_dict


def get_fame(item):
    if item == 'armor':
        fame = ARMOR_FAME
    elif item == 'sandals':
        fame = SANDALS_FAME
    elif item == 'crossbow':
        fame = CROSSBOW_FAME
    return fame
