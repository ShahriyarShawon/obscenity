fun multiply(x, y) {
    return .x * .y
}

fun squared(x) {
    return .x * .x
}

fun tripled(x) {
    return 3 * .x
}


fun init() {
    var a 
    var b
    var c
    var d

    a : 1
    b : 3
    c : .a + .b

    iprint(.c)
    sprint("\n")
    d : multiply(.b, .c)
    iprint(.d)
    
}
