describe("App", () => {
  beforeEach(() => {
    cy.visit("/");
  });
  it("test casm homepage", () => {
    cy.get("h1").should(
      "have.text",
      "CASM - Computational Analysis of Systems Metabolism"
    );
  });
  it("test navigation", () => {
    cy.contains("Atom Transition").click();
    cy.url().should("include", "/atom-transition");
  });
});
