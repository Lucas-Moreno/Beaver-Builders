const chai = require("chai");
const { expect } = chai;

describe("Basic Tests", () => {
  it("should add two numbers correctly", () => {
    const result = 2 + 3;
    expect(result).to.equal(5);
  });

  it("should return 0 when adding 0 to a number", () => {
    const result = 0 + 7;
    expect(result).to.equal(7);
  });
});
