import "@testing-library/jest-dom";

// Jest globals
declare global {
  var describe: jest.Describe;
  var it: jest.It;
  var expect: jest.Expect;
  var test: jest.It;
  var beforeEach: jest.Lifecycle;
  var afterEach: jest.Lifecycle;
  var beforeAll: jest.Lifecycle;
  var afterAll: jest.Lifecycle;
}
