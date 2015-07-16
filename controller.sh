#!/bin/bash
printf "\nWelcome to the Magento API Explorer! Select an option:\n\n"

MainAction () {
	if [[ "$1" == 'category.info' ]] ; then
		printf "Enter the ID of the categoryq. "
		read -p '> ' asset_id
	fi

	if [[ "$1" == 'product.info' ]] ; then
		printf "Enter the ID of the product. "
		read -p '> ' asset_id
	fi

	if [[ "$1" == 'configurable' ]] ; then
		asset_id="lol"
	fi

	printf "Loading..."
	python api_client_magento.py "$1" $asset_id > dummy_file.py
	pygmentize dummy_file.py | less -R
	printf "\n\n"
}

CustomAction () {
	printf "Enter the resource. "
	read -p '> ' resource

	printf "Enter the id. "
	read -p '> ' id

	printf "Loading..."
	python api_client_magento.py $resource $id > dummy_file.py
	pygmentize dummy_file.py | less -R
	printf "\n\n"	
}

PS3="> "
COLUMNS=2
select yn in "Category Tree" "Category By Id" "Product By Id" "Random Product" "Configurable" "Custom Call" "Quit"
do
    case $yn in
        "Category Tree" ) MainAction "category.tree" ; ;;
		"Category By Id" ) MainAction "category.info" ; ;;
		"Product By Id" ) MainAction "product.info" ; ;;
        "Random Product" ) MainAction "product.info" ; ;;
		"Configurable" ) MainAction "configurable" ; ;;
		"Custom Call" ) CustomAction ; ;;
		"Quit" ) break;;
    esac
done

PromptUserForAssetId () {
	read -p "Please type the ID of the product and press ENTER." asset_id
	return $asset_id
}