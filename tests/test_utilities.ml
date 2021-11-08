
let print_list print_func l =
  let rec printer = function
      | [] -> ()
      | [ e ] ->
          print_func e;
          print_string " "
      | e :: q ->
          print_func e;
          print_string "; ";
          printer q
  in
  print_string "[ ";
  printer l;
  print_string "]"

let print_couple_int (a, b) =
  print_string "(";
  print_int a;
  print_string ",";
  print_int b;
  print_string ")"

let rec print_mat print_func = function
    | [] -> ()
    | [ l ] ->
        print_string "\n\t[";
        (print_list print_func) l;
        print_string "]"
    | l :: mat ->
        print_string "\n\t[";
        (print_list print_func) l;
        print_string "];";
        print_mat print_func mat

let test print_func actual expected error_msg =
  if actual <> expected then (
    print_string "\027[31m\t";
    print_string error_msg;
    print_string "\n\tExpected ";
    print_func expected;
    print_string " but got ";
    print_func actual;
    print_string ".\n";
    print_string "\027[0m"
  ) else
    print_string "\027[34m";
  print_string "OK";
  print_string "\027[0m";
  print_endline (" " ^ error_msg)

let test_list print_func =
  let print_list_wrap l =
    print_string "[";
    print_list print_func l;
    print_string "]"
  in
  test print_list_wrap

let test_int = test print_int

let test_char = test print_char

let print_bool b = print_string (string_of_bool b)

let test_bool = test print_bool

let test_exception func_to_run error_msg =
  try func_to_run () with
  | Stdlib.Invalid_argument a ->
      print_string "\027[34m";
      print_string "OK";
      print_string "\027[0m"
  | _ ->
      print_string "\027[31m\t";
      print_string error_msg;
      print_string "\n\tExpected Invalid_argument.\n";
      print_string "\027[0m"

let test_int_list = test_list print_int
let test_char_list = test_list print_char

let test_couple_int_list = test_list print_couple_int

let test_mat print_func =
  let print_mat_wrap m =
    print_string "[";
    print_mat print_func m;
    print_string "]"
  in
  test print_mat_wrap
