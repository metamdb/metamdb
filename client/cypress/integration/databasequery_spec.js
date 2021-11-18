/// <reference types="Cypress" />

describe("databaseQuery reactions", () => {
  beforeEach(() => {
    //fixtures
    cy.fixture("autocomplete/reaction_alanine.json").as("alanineAutoJson");
    cy.fixture("autocomplete/feed_aminotransferase.json").as(
      "aminotransferaseJson"
    );
    cy.fixture("autocomplete/feed_al.json").as("alJson");

    cy.visit("/");
    cy.get("h1").contains("MetAMDB - Metabolic Atom Mapping Database");
    cy.visit("/database-query");
  });

  it("user searches for reactions and clicks on autocomplete", () => {
    // network stubs
    const serverUrl = Cypress.env("serverUrl");
    cy.intercept(`${serverUrl}/api/suggestions/reactions?q=al`, {
      fixture: "autocomplete/reaction_alanine.json",
    }).as("getSuggestion");
    cy.intercept("POST", `${serverUrl}/api/query`, {
      fixture: "autocomplete/feed_aminotransferase.json",
    }).as("postQuery");

    // check if reaction checked
    cy.findByRole("combobox").find(":selected").contains("Reaction");

    // write in searchbox
    cy.findByRole("textbox", { name: /reaction/i }).type("al");

    cy.findByRole("button", {
      name: /aladehydchloro\-rxn \(metacyc\)/i,
    }).should("be.visible");

    // click suggestion
    cy.findByRole("button", {
      name: /alanine\-aminotransferase\-rxn \(metacyc\)/i,
    })
      .should("be.visible")
      .click();
    cy.findByRole("textbox", { name: /reaction/i }).should(
      "have.value",
      "ALANINE-AMINOTRANSFERASE-RXN"
    );

    // click reaction
    cy.findByRole("link", { name: /6941/i })
      .should("have.attr", "target", "_blank")
      .invoke("removeAttr", "target")
      .click();
  });

  it("user searches for reactions and enters", () => {
    // network stubs
    const serverUrl = Cypress.env("serverUrl");
    cy.intercept(`${serverUrl}/api/suggestions/reactions?q=al`, {
      fixture: "autocomplete/reaction_alanine.json",
    }).as("getSuggestion");
    cy.intercept("POST", `${serverUrl}/api/query`, {
      fixture: "autocomplete/feed_al.json",
    }).as("postQuery");

    // check if reaction checked
    cy.findByRole("combobox").find(":selected").contains("Reaction");

    // write in searchbox
    cy.findByRole("textbox", { name: /reaction/i }).type("al");

    cy.findByRole("button", {
      name: /aladehydchloro\-rxn \(metacyc\)/i,
    }).should("be.visible");

    // click suggestion
    cy.findByRole("button", {
      name: /alanine\-aminotransferase\-rxn \(metacyc\)/i,
    }).should("be.visible");

    cy.findByRole("textbox", { name: /reaction/i }).type("{enter}");

    cy.findByRole("textbox", { name: /reaction/i }).should("have.value", "al");

    // click pagination
    cy.findByRole("button", { name: /50/i }).click();
    cy.findByRole("menuitem", { name: /25/i }).click();
  });
});
