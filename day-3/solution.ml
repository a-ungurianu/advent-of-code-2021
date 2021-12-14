open Stdio

let explode input =
  let rec aux idx lst =
    if idx<0 then lst else aux (idx-1) (input.[idx] :: lst)
  in aux (String.length input - 1) []

let int_of_binary_char c = int_of_char c - int_of_char '0'

let nth_col n xs = let getNth xs =List.nth xs n in  List.map getNth xs;;

let first_col xs = nth_col 0 xs;;

let rec transpose xss = match xss with
  | []::_ -> []
  | things -> (first_col things)::(transpose (List.map List.tl things)) 


let freq xs = 
  let rec _freq xs zeros ones = match xs with
    | 0::xs -> _freq xs (zeros + 1) ones 
    | 1::xs -> _freq xs zeros (ones + 1)
    | _::_ -> failwith "Unexpected number"
    | [] -> (zeros, ones)
  in _freq xs 0 0

let choose (zeros, ones) = if ones >= zeros  then 1 else 0;;
let chooseNot (zeros, ones) = if zeros <= ones then 0 else 1;;

let epsilonBit xs = chooseNot @@ freq @@ xs;;
let gammaBit xs = choose @@ freq @@ xs;;

let int_of_bin_int xs = 
  let rec _f xs acc = match xs with
    | x::xs -> _f xs (Base.Int.shift_left acc 1 + x)
    | [] -> acc in _f xs 0

let extractData data f = data |> transpose |> List.map f |> int_of_bin_int;;

let processLine line = line |> explode |> List.map int_of_binary_char;;

let data = In_channel.input_lines( open_in "./input") |> List.map processLine ;;

let gamma = extractData data gammaBit;;
let epsilon = extractData data epsilonBit;;

Printf.printf "First answer: %d\n" (gamma * epsilon);;

let filter_by_idx idx v xss = let shouldKeep xs = v == (List.nth xs idx) in List.filter shouldKeep xss;; 

let extractData2 data f = let rec _extractData2 i xss = 
                        if List.length xss > 1 
                        then let most_first = f @@ freq @@ nth_col i @@ xss in _extractData2 (i + 1) (xss |> filter_by_idx i most_first) 
                        else (List.hd xss) in _extractData2 0 data;;

let o2_extract data = extractData2 data choose;;

let co2_extract data = extractData2 data chooseNot;;


let o2_value = data |> o2_extract |> int_of_bin_int;;
let co2_value = data |> co2_extract |> int_of_bin_int;;

Printf.printf "O2: %d CO2: %d Result: %d\n" o2_value co2_value (o2_value * co2_value);;

