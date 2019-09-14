pragma solidity >=0.5.0 <0.6.0;

contract Demo {
    uint public value = 42;

    event Acted(uint value, uint timestamp);

    function compare(uint arg) public view returns (bool, bool) {
        return (value > arg, value < arg);
    }

    function act() public {
        value++;
        emit Acted(value, now);
    }

    function set(uint oldValue, uint newValue) public {
        require(value == oldValue);
        value = newValue;
    }

    function teardown(address payable who) public {
        selfdestruct(who);
    }
}
