import { useState, useEffect } from 'react';
import { Combobox } from '@headlessui/react';
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/24/outline';
import { ceremonyTypesApi } from '../../../shared/api/ceremonyTypes';
import type { CeremonyType } from '../../../shared/api/ceremonyTypes';

interface CeremonyTypeSelectorProps {
  value?: number;
  onChange: (value: number | null) => void;
}

export function CeremonyTypeSelector({ value, onChange }: CeremonyTypeSelectorProps) {
  const [query, setQuery] = useState('');
  const [types, setTypes] = useState<CeremonyType[]>([]);

  useEffect(() => {
    ceremonyTypesApi.getAll().then(res => setTypes(res.data));
  }, []);

  const filteredTypes = query === ''
    ? types
    : types.filter(t => t.name.toLowerCase().includes(query.toLowerCase()));

  const selected = types.find(t => t.id === value);

  return (
    <Combobox value={selected} onChange={(type) => onChange(type?.id || null)}>
      <div className="relative">
        <Combobox.Input
          className="w-full rounded-xl border border-border bg-white py-3 pl-4 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/30"
          displayValue={(type: CeremonyType | null) => type?.name || ''}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Rechercher un type de cérémonie..."
        />
        <Combobox.Button className="absolute inset-y-0 right-0 flex items-center pr-2">
          <ChevronUpDownIcon className="h-5 w-5 text-gray-400" />
        </Combobox.Button>

        <Combobox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-xl bg-white py-1 shadow-lg border border-border">
          {filteredTypes.map((type) => (
            <Combobox.Option
              key={type.id}
              value={type}
              className={({ active }) =>
                `cursor-default select-none py-2 pl-10 pr-4 ${
                  active ? 'bg-primary-50 text-primary-900' : 'text-gray-900'
                }`
              }
            >
              {({ selected, active }) => (
     <>
                  <span className={`block truncate ${selected ? 'font-medium' : 'font-normal'}`}>
                    {type.name}
                  </span>
                  {selected ? (
                    <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-primary-600">
                      <CheckIcon className="h-5 w-5" />
                    </span>
                  ) : null}
                </>
              )}
            </Combobox.Option>
          ))}
        </Combobox.Options>
      </div>
    </Combobox>
  );
}