#!/usr/bin/env python3

from get_data import ExtractAndSaveNbaData 
from utils import save_in_df

def main():
    ExtractAndSaveNbaData("2022").save()



if __name__ == "__main__":
    main()
