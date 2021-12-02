open Stdio

let rec zip (l1, l2) =
  match l1, l2 with
  | f1::r1, f2::r2 -> (f1,f2)::zip(r1, r2)
  | _ , _-> [];;

let rec zip3 (l1, l2, l3) =
  match l1, l2, l3 with
  | f1::r1, f2::r2, f3::r3 -> (f1,f2,f3)::zip3(r1, r2, r3)
  | _ , _, _ -> [];;

let sum3 (a,b,c) = a + b + c;;

let is_increasing (a,b) : bool = a < b;;

let get_increasing_count l = 
  let paired = zip(l, List.tl(l)) in
  let filtered = List.filter is_increasing paired in
  List.length filtered;;


let numbers = List.map int_of_string (In_channel.input_lines( open_in "./input"));;

let num_increasing = get_increasing_count numbers;;

print_string "Number of increasing values is: ";;
print_int num_increasing;;
print_string "\n";;

let rolling_sum3 = List.map sum3 (zip3(numbers,List.tl(numbers), List.tl(List.tl(numbers))));;

let rolling_num_increasing = get_increasing_count rolling_sum3;;

print_string "Number of increasing values in rolling sum is: ";;
print_int num_increasing;;
print_string "\n";;
