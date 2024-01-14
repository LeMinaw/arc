export const capitalize = str => str.charAt(0).toUpperCase() + str.substring(1)

export const isDigit = str => str.length == 1 && str >= "0" && str <= "9"
