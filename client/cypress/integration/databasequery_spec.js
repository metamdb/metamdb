/// <reference types="Cypress" />

describe("databaseQuery", () => {
  beforeEach(() => {
    //fixtures
    cy.fixture("autocomplete/reaction_alanine.json").as("alanineAutoJson");

    cy.visit("/");
    cy.get("h1").contains("MetAMDB - Metabolic Atom Mapping Database");
    cy.visit("/database-query");
  });

  it("user can search for reactions", () => {
    //network stubs
    const serverUrl = Cypress.env("serverUrl");
    cy.intercept(`${serverUrl}/api/suggestions/reactions?q=al`, {
      fixture: "autocomplete/reaction_alanine.json",
    }).as("getSuggestion");

    //check if reaction checked
    cy.findByRole("combobox").find(":selected").contains("Reaction");

    //write in searchbox
    cy.findByRole("textbox", { name: /reaction/i }).type("al");
  });
});
