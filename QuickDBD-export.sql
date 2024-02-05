-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/tpxlDU
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


SET XACT_ABORT ON

BEGIN TRANSACTION QUICKDBD

CREATE TABLE [Ratings] (
    [YMM] varchar  NOT NULL ,
    [year_make-model] varchar  NOT NULL ,
    [make] varchar  NOT NULL ,
    [model_year] int  NOT NULL ,
    [rollover] int  NOT NULL ,
    [safety_concerns] boolean  NOT NULL ,
    CONSTRAINT [PK_Ratings] PRIMARY KEY CLUSTERED (
        [YMM] ASC
    )
)

CREATE TABLE [Recalls] (
    [recalls] vachar  NOT NULL ,
    [Year_make_model] varchar  NOT NULL ,
    [manufacturer] varchar  NOT NULL ,
    [base_model] varchar  NOT NULL ,
    [model] varchar  NOT NULL ,
    [model_year] int  NOT NULL ,
    [NHTSA_campaign_number] int  NOT NULL ,
    [parklt] varchar  NOT NULL ,
    [parkOutside] varchar  NOT NULL ,
    [NHTSA_action_number] int  NOT NULL ,
    [report_received_data] varchar  NOT NULL ,
    [component] varchar  NOT NULL ,
    [summary] varchar  NOT NULL ,
    [consequence] varchar  NOT NULL ,
    [remedy] varchar  NOT NULL ,
    CONSTRAINT [PK_Recalls] PRIMARY KEY CLUSTERED (
        [Year_make_model] ASC,[NHTSA_campaign_number] ASC
    )
)

CREATE TABLE [Complaints] (
    [complaints] varchar  NOT NULL ,
    [year_mnake_model] varchar  NOT NULL ,
    [manufacturer] varchar  NOT NULL ,
    [base_model] varchar  NOT NULL ,
    [model_year] int  NOT NULL ,
    [type] varchar  NOT NULL ,
    [ODI_number] int  NOT NULL ,
    [crash] boolean  NOT NULL ,
    [fire] boolean  NOT NULL ,
    [number_of_injuries] int  NOT NULL ,
    [number_of_deaths] int  NOT NULL ,
    [date_of_incident] date  NOT NULL ,
    [date_complaint_filed] date  NOT NULL ,
    [VIN] varchar  NOT NULL ,
    [components] varchar  NOT NULL ,
    [summary] varchar  NOT NULL 
)

CREATE TABLE [Vehicles] (
    [year_make_model] varchar  NOT NULL ,
    [make] varchar  NOT NULL ,
    [base_model] varchar  NOT NULL ,
    [model_year] varchar  NOT NULL 
)

ALTER TABLE [Ratings] WITH CHECK ADD CONSTRAINT [FK_Ratings_year_make-model] FOREIGN KEY([year_make-model])
REFERENCES [Vehicles] ([year_make_model])

ALTER TABLE [Ratings] CHECK CONSTRAINT [FK_Ratings_year_make-model]

ALTER TABLE [Complaints] WITH CHECK ADD CONSTRAINT [FK_Complaints_year_mnake_model_model_year] FOREIGN KEY([year_mnake_model], [model_year])
REFERENCES [Vehicles] ([year_make_model], [model_year])

ALTER TABLE [Complaints] CHECK CONSTRAINT [FK_Complaints_year_mnake_model_model_year]

ALTER TABLE [Vehicles] WITH CHECK ADD CONSTRAINT [FK_Vehicles_year_make_model] FOREIGN KEY([year_make_model])
REFERENCES [Recalls] ([Year_make_model])

ALTER TABLE [Vehicles] CHECK CONSTRAINT [FK_Vehicles_year_make_model]

ALTER TABLE [Vehicles] WITH CHECK ADD CONSTRAINT [FK_Vehicles_make] FOREIGN KEY([make])
REFERENCES [Ratings] ([make])

ALTER TABLE [Vehicles] CHECK CONSTRAINT [FK_Vehicles_make]

COMMIT TRANSACTION QUICKDBD