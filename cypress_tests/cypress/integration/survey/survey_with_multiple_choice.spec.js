describe("Survey with multiple options tests", () => {
    const url = "/en/sections/questionnaire-testing/sample-survey/";

    it("Visits the survey page", () => {
        cy.visitUrl(url)
    });

    it("Checks for the title text", () => {
        cy.testTitle(
            "Survey with multiple choice options",
            ".survey-page__title"
        );
    });

    it("It checks for the description text", () => {
        cy.testDescription(
            "intro text",
            ".survey-page__description>.block-paragraph>p"
        );
    });

    it("Checks for the question number text", () => {
        let questionNumbers = []
        cy.get(".quest-item__number").each(($el, index) => {
            questionNumbers.push($el)
        });
        cy.get(".quest-item__number").each(($el, index) => {
            cy.wrap($el)
                .should("be.visible")
                .contains(`${index + 1} of ${questionNumbers.length} questions`)
        });
    });

    it("Checks for the input types", () => {
        cy.get("[name=number_field_required]").each($el => {
            cy.wrap($el)
                .should("have.attr", "type", "checkbox")
                .should("be.visible");
        });

        cy.get("[type=radio]").each($el => {
            cy.wrap($el).should("be.visible");
        });
    });

    it("Selects the answers", () => {
        cy.get("[id=id_number_field_required_0]").click();
        cy.get("[id=id_dropdown_field_0]").check();
    });

    it("Submits the answers", () => {
        cy.submit(".survey-page__btn>span", "Submit");
    });

    it("Checks for successful redirection", () => {
        cy.url().should(
            "include",
            `/?back_url=${url}&form_length=3`
        );

        cy.thanksText(".block-paragraph", "thanks text");

        cy.submit(".survey-page__btn>span", "Back");
    });
});