ALTER TABLE members
ADD received_peeps INTEGER DEFAULT (0);

ALTER TABLE members
ADD sent_peeps INTEGER DEFAULT(0);