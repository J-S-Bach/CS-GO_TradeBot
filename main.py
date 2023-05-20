from trade_logic.dealing import get_profitable_offers


def main():
    for offer in get_profitable_offers():
        print(offer.profit)


if __name__ == '__main__':
    main()
