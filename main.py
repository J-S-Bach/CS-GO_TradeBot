from api.buff import api


def main():
    buffMarketplace = api.BuffMarketplace()
    buffMarketplace.getItemDetail(name="Glove Case")
t

if __name__ == '__main__':
    main()
