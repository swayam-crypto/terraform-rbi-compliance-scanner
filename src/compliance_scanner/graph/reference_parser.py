class ReferenceParser:

    def _normalize_resource_name(
        self,
        resource_name: str,
    ) -> str:
        """
        Remove Terraform index expressions from a resource name.

        Examples:
            private -> private
            private[0] -> private
            private[*] -> private
            private[count.index] -> private
            private[each.key] -> private
        """

        return resource_name.split("[", 1)[0]

    def _flatten_values(
        self,
        value: object,
    ) -> list[str]:
        """
        Recursively flatten Terraform values into a list of strings.
        """

        if isinstance(value, str):
            return [value]

        if isinstance(value, (list, tuple)):
            values: list[str] = []

            for item in value:
                values.extend(self._flatten_values(item))

            return values

        return []

    def parse_references(
        self,
        value: object,
    ) -> list[tuple[str, str]]:
        """
        Parse one or more Terraform resource references.

        Examples:
            "aws_subnet.private.id"
                -> [("aws_subnet", "private")]

            [
                "aws_security_group.web.id",
                "aws_security_group.db.id",
            ]
                -> [
                    ("aws_security_group", "web"),
                    ("aws_security_group", "db"),
                ]
        """

        references: list[tuple[str, str]] = []

        values = self._flatten_values(
            value,
        )

        for item in values:
            parts = item.split(".")

            if len(parts) < 2:
                continue

            resource_type = parts[0]

            resource_name = self._normalize_resource_name(
                parts[1],
            )

            references.append(
                (
                    resource_type,
                    resource_name,
                )
            )

        return references
