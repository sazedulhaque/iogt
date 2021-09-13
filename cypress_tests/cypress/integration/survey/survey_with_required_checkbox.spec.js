describe("Survey with required checkbox tests", () => {
    const url = "/en/sections/questionnaire-testing/survey-with-checkbox-req/";

    it("Visits the survey page", () => {
        cy.visitUrl(url);
    });

    it("Checks for the title text", () => {
        cy.testTitle(
            "Survey with required checkbox",
            ".survey-page__title"
        );
    });

    it("It checks for the description text", () => {
        cy.testDescription(
            "intro",
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
                .contains(`${index + 1} of ${questionNumbers.length} question`);
        });
    });

    it("Checks for help text", () => {
        cy.get(".quest-item__step-desc span")
            .contains("Check if apply")
            .should("be.visible");
    });

    it("submits unchecked form", () => {
        cy.get(".survey-page__btn>span")
            .contains("Submit")
            .should("be.visible")
            .click();

        cy.url().should("include", url);
    });


    it("Checks the checkbox", () => {
        cy.get("[name=checkbox]").check();
    })

    it("Submits the form", () => {
        cy.submit(".survey-page__btn>span", "Submit");
    });

    it("Checks for successful redirection", () => {
        cy.url().should(
            "include",
            `/?back_url=${url}&form_length=1`
        );

        cy.thanksText(".block-paragraph", "thanks");
        cy.submit(".survey-page__btn>span", "Back");
    });

});