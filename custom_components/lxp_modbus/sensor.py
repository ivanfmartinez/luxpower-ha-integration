    @property
    def native_value(self):
        """Return the state of the sensor."""
        
        # First, check if the coordinator has any data yet.
        if not self.coordinator.data:
            return None

        raw_val = None

        # Determine the raw (unscaled) value based on sensor type
        if self._desc.get("register_type") == "calculated":
            input_data = self.coordinator.data.get("input", {})
            calculation_func = self._desc["extract"]
            raw_val = calculation_func(input_data, self._entry)
        else:
            # For standard register-based sensors:
            registers = self.coordinator.data.get(self._register_type, {})
            value = registers.get(self._register)
            if value is not None:
                # Extract the raw value using the lambda from the description
                raw_val = self._desc["extract"](value)

        # If we couldn't determine a raw value, return None
        if raw_val is None:
            return None

        # 1. Handle sensors that map a code to a text option
        if "options" in self._desc:
            return self._desc["options"].get(raw_val, self._desc.get("default", "Unknown"))

        # 2. Handle numerical sensors that require scaling
        if "scale" in self._desc:
            scale = self._desc["scale"]
            scaled_value = raw_val * scale
            # Return a clean int if it's a whole number, otherwise a float
            return int(scaled_value) if scaled_value == int(scaled_value) else scaled_value

        # 3. For any other sensor (like free-form text), return the raw value directly
        return raw_val